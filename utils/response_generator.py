import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Optional
import json
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

class ResponseGenerator:
    def __init__(self, model_path: str, device: str = None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Loading model on {self.device}...")
        
        try:
            # Check if this is a PEFT adapter
            adapter_config_path = os.path.join(model_path, "adapter_config.json")
            
            if os.path.exists(adapter_config_path):
                print("Detected PEFT adapter, loading with proper PEFT support...")
                
                # Load adapter config to get base model
                with open(adapter_config_path, 'r') as f:
                    adapter_config = json.load(f)
                
                base_model_name = adapter_config.get("base_model_name_or_path", "microsoft/phi-2")
                print(f"Base model: {base_model_name}")
                
                # Load tokenizer from base model (to avoid corrupted tokenizer)
                print("Loading tokenizer from base model...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    base_model_name, 
                    trust_remote_code=True,
                    use_fast=False  # Use slow tokenizer to avoid issues
                )
                
                # Load base model
                print(f"Loading base model: {base_model_name}")
                base_model = AutoModelForCausalLM.from_pretrained(
                    base_model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map={"": self.device} if self.device == "cuda" else None,
                    trust_remote_code=True,
                    attn_implementation="eager"  # Use eager attention
                )
                
                # Try to load PEFT properly
                try:
                    from peft import PeftModel, PeftConfig
                    print(f"Loading PEFT adapter from: {model_path}")
                    
                    # Try loading with proper config
                    peft_config = PeftConfig.from_pretrained(model_path)
                    self.model = PeftModel.from_pretrained(base_model, model_path, config=peft_config)
                    print("✅ PEFT adapter loaded successfully!")
                    
                except Exception as peft_error:
                    print(f"⚠️ PEFT loading failed: {peft_error}")
                    print("Trying alternative PEFT loading...")
                    
                    # Alternative: Load directly without explicit config
                    try:
                        from peft import PeftModel
                        # Create a temporary directory with just the adapter weights
                        import tempfile
                        import shutil
                        
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Copy necessary files
                            for file_name in ['adapter_model.safetensors', 'adapter_config.json']:
                                src = os.path.join(model_path, file_name)
                                if os.path.exists(src):
                                    shutil.copy2(src, temp_dir)
                            
                            self.model = PeftModel.from_pretrained(base_model, temp_dir)
                            print("✅ PEFT adapter loaded with alternative method!")
                    
                    except Exception as alt_error:
                        print(f"⚠️ Alternative PEFT loading also failed: {alt_error}")
                        print("Using manual LoRA integration...")
                        
                        # Manual LoRA loading and integration
                        try:
                            import safetensors
                            adapter_weights_path = os.path.join(model_path, "adapter_model.safetensors")
                            
                            if os.path.exists(adapter_weights_path):
                                print("Found adapter weights, attempting manual integration...")
                                
                                # Load adapter weights
                                adapter_weights = safetensors.torch.load_file(adapter_weights_path)
                                
                                # Get model state dict
                                model_state_dict = base_model.state_dict()
                                
                                # Apply LoRA weights manually
                                lora_rank = adapter_config.get("r", 8)
                                lora_alpha = adapter_config.get("lora_alpha", 16)
                                scaling = lora_alpha / lora_rank
                                
                                print(f"Applying LoRA weights with rank={lora_rank}, alpha={lora_alpha}, scaling={scaling}")
                                
                                # Group LoRA weights by layer and module
                                lora_weights = {}
                                for key, weight in adapter_weights.items():
                                    if "lora_A" in key or "lora_B" in key:
                                        # Extract base key (remove lora_A/lora_B suffix)
                                        base_key = key.replace(".lora_A.weight", "").replace(".lora_B.weight", "")
                                        if base_key not in lora_weights:
                                            lora_weights[base_key] = {}
                                        
                                        if "lora_A" in key:
                                            lora_weights[base_key]["A"] = weight
                                        else:
                                            lora_weights[base_key]["B"] = weight
                                
                                # Apply LoRA updates to model weights
                                updated_params = 0
                                for base_key, lora_pair in lora_weights.items():
                                    if "A" in lora_pair and "B" in lora_pair:
                                        # Remove the "base_model.model." prefix to match state dict keys
                                        model_key = base_key.replace("base_model.model.", "") + ".weight"
                                        
                                        if model_key in model_state_dict:
                                            original_weight = model_state_dict[model_key]
                                            lora_A = lora_pair["A"].to(original_weight.device)
                                            lora_B = lora_pair["B"].to(original_weight.device)
                                            
                                            # Apply LoRA: W = W₀ + BA * scaling
                                            delta_w = torch.mm(lora_B, lora_A) * scaling
                                            new_weight = original_weight + delta_w
                                            
                                            # Update the model parameter
                                            with torch.no_grad():
                                                model_state_dict[model_key].copy_(new_weight)
                                            
                                            updated_params += 1
                                            print(f"Updated parameter: {model_key}")
                                
                                print(f"✅ Successfully applied {updated_params} LoRA parameter updates!")
                                self.model = base_model
                                
                            else:
                                print("No adapter weights found, using base model")
                                self.model = base_model
                                
                        except Exception as manual_error:
                            print(f"Manual loading also failed: {manual_error}")
                            print("Using base model only - your training won't be applied")
                            self.model = base_model
                
            else:
                print("Loading as regular model...")
                # Load as regular model
                self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map={"": self.device} if self.device == "cuda" else None,
                    trust_remote_code=True
                )
        
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Ensure we have a proper pad token
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print(f"❌ Error details: {type(e).__name__}: {str(e)}")
            raise e
    
    def is_general_greeting(self, prompt: str) -> bool:
        """Check if the prompt is a general greeting that was trained"""
        greetings = [
            'hi', 'hello', 'good morning', 'hey', 'good afternoon', 
            'hi there', 'good evening', 'morning', 'hello!', 'hey there',
            'greetings', 'hi chatbot', "what's up", 'hi, i need help', 'good day'
        ]
        return prompt.lower().strip() in greetings
    
    def is_thank_you_message(self, prompt: str) -> bool:
        """Check if the prompt is a thank you message"""
        thank_you_phrases = [
            'thank you', 'thanks', 'thank you so much', 'thanks a lot',
            'thank you very much', 'appreciate it', 'thanks for your help',
            'thank you for the information', 'thanks for helping', 'grateful',
            'thank you for the help', 'thanks for the info', 'much appreciated',
            'thank you!', 'thanks!', 'thx', 'ty', 'cheers'
        ]
        prompt_lower = prompt.lower().strip()
        return any(phrase in prompt_lower for phrase in thank_you_phrases)
    
    def generate_response(self, prompt: str, similar_qa: List[Dict] = None,
                         max_length: int = 150, temperature: float = 0.7) -> str:
        """Generate response using the fine-tuned model"""
        
        try:
            # PRIORITY: For greetings, use direct responses immediately (no generation)
            if self.is_general_greeting(prompt):
                print(f"🎯 Detected general greeting: {prompt}")
                print(f"🚀 Using direct trained response for CPU performance")
                # Use your exact trained responses directly
                direct_responses = {
                    'hi': "Hello! Would you like information about Galaxy Organisation's programs or Alibaba's services today?",
                    'hello': "Hi there! Are you interested in Galaxy Organisation or Alibaba?",
                    'good morning': "Good morning! How can I help? Ask about Galaxy's community programs or Alibaba's business solutions.",
                    'hey': "Hello! What can I assist with - Galaxy Organisation or Alibaba?",
                    'good afternoon': "Good afternoon! Shall we discuss Galaxy's initiatives or Alibaba's offerings?",
                    'hi there': "Hello! Exploring Galaxy Organisation or Alibaba today?",
                    'good evening': "Good evening! Are you looking for Galaxy Organisation details or Alibaba information?",
                    'morning': "Morning! What shall we cover - Galaxy Organisation or Alibaba?",
                    'hello!': "Hi! Curious about Galaxy's social impact or Alibaba's technology?",
                    'hey there': "Hello! Galaxy Organisation or Alibaba - what interests you today?",
                    'greetings': "Greetings! Shall we focus on Galaxy Organisation or Alibaba?",
                    'hi chatbot': "Hello! Ready to discuss Galaxy's initiatives or Alibaba's services?",
                    "what's up": "Hello! Here to explore Galaxy Organisation or Alibaba?",
                    'hi, i need help': "Hello! Happy to help. Is this about Galaxy Organisation or Alibaba?",
                    'good day': "Good day! Asking about Galaxy's community work or Alibaba's business tools?"
                }
                
                response = direct_responses.get(prompt.lower().strip(), 
                    "Hello! How can I help you with Galaxy Organisation or Alibaba today?")
                print(f"✅ Direct response: {response[:100]}...")
                return response

            # NEW: Handle thank you messages
            if self.is_thank_you_message(prompt):
                print(f"🙏 Detected thank you message: {prompt}")
                print(f"🚀 Using direct thank you response")
                thank_you_responses = [
                    "You're very welcome! Feel free to ask if you need any more information about Galaxy Organisation or Alibaba services.",
                    "Happy to help! If you have any other questions about our programs or certifications, just let me know.",
                    "My pleasure! Don't hesitate to ask if you need more details about Galaxy's initiatives or Alibaba Cloud.",
                    "You're welcome! I'm here whenever you need assistance with Galaxy Organisation or Alibaba questions.",
                    "Glad I could help! Feel free to reach out anytime for more information about our training programs.",
                    "No problem at all! Ask me anything else about Galaxy Organisation or Alibaba services.",
                    "You're most welcome! I'm always here to help with Galaxy and Alibaba information."
                ]
                import random
                response = random.choice(thank_you_responses)
                print(f"✅ Thank you response: {response[:100]}...")
                return response

            # For non-greeting questions, use model generation (slower)
            if similar_qa and len(similar_qa) > 0:
                # Use context from similar Q&As
                context = ""
                for qa, score in similar_qa[:1]:  # Only use 1 example for speed
                    if score > 0.7:
                        context += f"Example: {qa['prompt']} -> {qa['completion']}\n"
                
                if context:
                    formatted_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:"
                else:
                    formatted_prompt = prompt
            else:
                formatted_prompt = prompt
            
            print(f"📝 Using question format: {formatted_prompt[:100]}...")
            # Use greedy generation for questions too
            generation_params = {
                'max_new_tokens': 30,     # Short responses
                'do_sample': False,       # Greedy (fastest)
                'early_stopping': True,
                'use_cache': True
            }
            
            # Tokenize with minimal settings for speed
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=100,  # Very short for maximum speed
                padding=False    # No padding for speed
            ).to(self.device)
            
            print(f"🔧 Input length: {inputs.input_ids.shape[1]} tokens")
            print(f"⚙️ Generation params: {generation_params}")
            print(f"💻 Running on {self.device} - using GREEDY generation for maximum speed")
            
            # Generate with minimal parameters for maximum speed
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,  # Only pass input_ids for speed
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    **generation_params
                )
            
            # Decode response
            input_length = inputs.input_ids.shape[1]
            response_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(response_tokens, skip_special_tokens=True)
            
            print(f"🔍 Raw response: {response[:150]}...")
            
            # Clean up response based on type
            if self.is_general_greeting(prompt):
                # For greetings, the response should be direct
                response = response.strip()
                
                # Remove the input prompt if it appears in output
                if formatted_prompt in response:
                    response = response.replace(formatted_prompt, "").strip()
                
                # Remove common prefixes that might appear
                prefixes_to_remove = ["<GENERAL>", prompt.lower(), prompt.upper(), prompt]
                for prefix in prefixes_to_remove:
                    if response.lower().startswith(prefix.lower()):
                        response = response[len(prefix):].strip()
                
                # Remove leading punctuation or spaces
                response = response.lstrip('.,!?:; ')
                
            else:
                # For questions, clean more thoroughly
                if "Answer:" in response:
                    response = response.split("Answer:")[-1].strip()
                elif "Question:" in response:
                    response = response.split("Question:")[0].strip()
                
                # Remove artifacts
                artifacts = ["Context:", "Example:", formatted_prompt]
                for artifact in artifacts:
                    if artifact in response:
                        response = response.replace(artifact, "").strip()
            
            # Final cleanup
            response = self._clean_final_response(response, prompt, similar_qa)
            
            print(f"✅ Final response: {response[:100]}...")
            return response
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            import traceback
            traceback.print_exc()
            return self._get_fallback_response(prompt, similar_qa)
    
    def _clean_final_response(self, response: str, original_prompt: str, similar_qa: List[Dict] = None) -> str:
        """Final cleaning and validation of response"""
        
        # Remove extra whitespace and newlines
        response = ' '.join(response.split())
        
        # For greetings and thank you messages, be more lenient about response length
        min_length = 3 if (self.is_general_greeting(original_prompt) or self.is_thank_you_message(original_prompt)) else 5
        
        # If response is too short or empty, use fallback
        if len(response.strip()) < min_length:
            return self._get_fallback_response(original_prompt, similar_qa)
        
        # If response seems to repeat the question, use fallback
        if original_prompt.lower() in response.lower() and len(response) < 30:
            return self._get_fallback_response(original_prompt, similar_qa)
        
        # Limit response length
        if len(response) > 300:
            sentences = response.split('.')
            truncated = ''
            for sentence in sentences:
                if len(truncated + sentence + '.') <= 300:
                    truncated += sentence + '.'
                else:
                    break
            response = truncated.strip()
        
        return response
    
    def _get_fallback_response(self, prompt: str, similar_qa: List[Dict] = None) -> str:
        """Get fallback response when generation fails"""
        
        # For greetings, try to find from training data first
        if self.is_general_greeting(prompt):
            # Look for exact matches in similar_qa first
            if similar_qa:
                for qa, score in similar_qa:
                    if qa['prompt'].lower().strip() == f"<general>{prompt.lower().strip()}":
                        return qa['completion']
            
            # If no trained response found, use hardcoded fallbacks
            greeting_responses = {
                'hi': "Hello! Would you like information about Galaxy Organisation's programs or Alibaba's services today?",
                'hello': "Hi there! Are you interested in Galaxy Organisation or Alibaba?",
                'good morning': "Good morning! How can I help? Ask about Galaxy's community programs or Alibaba's business solutions.",
                'hey': "Hello! What can I assist with - Galaxy Organisation or Alibaba?",
                'good afternoon': "Good afternoon! Shall we discuss Galaxy's initiatives or Alibaba's offerings?",
                'hi there': "Hello! Exploring Galaxy Organisation or Alibaba today?",
                'good evening': "Good evening! Are you looking for Galaxy Organisation details or Alibaba information?",
                'morning': "Morning! What shall we cover - Galaxy Organisation or Alibaba?",
                'hello!': "Hi! Curious about Galaxy's social impact or Alibaba's technology?",
                'hey there': "Hello! Galaxy Organisation or Alibaba - what interests you today?",
                'greetings': "Greetings! Shall we focus on Galaxy Organisation or Alibaba?",
                'hi chatbot': "Hello! Ready to discuss Galaxy's initiatives or Alibaba's services?",
                "what's up": "Hello! Here to explore Galaxy Organisation or Alibaba?",
                'hi, i need help': "Hello! Happy to help. Is this about Galaxy Organisation or Alibaba?",
                'good day': "Good day! Asking about Galaxy's community work or Alibaba's business tools?",
                'good morning, how are you!': "Good morning! I'm doing well, thank you. Are you interested in Galaxy Organisation or Alibaba?"
            }
            
            return greeting_responses.get(prompt.lower().strip(), 
                "Hello! How can I help you with Galaxy Organisation or Alibaba today?")
        
        # For thank you messages
        if self.is_thank_you_message(prompt):
            return "You're welcome! Feel free to ask if you need any more information about Galaxy Organisation or Alibaba services."
        
        # For other questions, try similar Q&A first
        if similar_qa and len(similar_qa) > 0:
            best_match = similar_qa[0]
            if best_match[1] > 0.6:
                return best_match[0]['completion']
        
        # Default response for specific questions
        return "I specialize in questions about Galaxy Organisation and Alibaba Cloud services. Could you please ask about our training programs, certifications, or services?"
    
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate responses for multiple prompts"""
        responses = []
        for prompt in prompts:
            response = self.generate_response(prompt, **kwargs)
            responses.append(response)
        return responses
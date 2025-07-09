
import json
import re
from typing import List, Dict, Tuple

class DataProcessor:
    def __init__(self):
        self.galaxy_keywords = [
            'galaxy', 'galaxy organisation', 'galaxy organization', 
            'computers for schools', 'cfsp', 'women empowerment',
            'kids empowerment', 'electronics recycling', 'amman jordan'
        ]
        self.alibaba_keywords = [
            'alibaba', 'alibaba cloud', 'alibaba academy', 'aca', 'acp', 'ace',
            'cloud computing', 'maxcompute', 'dataworks', 'ecs', 'pai',
            'double 11', 'singles day', 'jack ma'
        ]
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Fix common typos
        text = text.replace('orgaanisation', 'organisation')
        text = text.replace('GENERAL', 'Alibaba')
        return text.strip()
    
    def categorize_question(self, question: str) -> str:
        """Determine if question is about Galaxy, Alibaba, or General"""
        question_lower = question.lower()
        
        galaxy_score = sum(1 for kw in self.galaxy_keywords if kw in question_lower)
        alibaba_score = sum(1 for kw in self.alibaba_keywords if kw in question_lower)
        
        if galaxy_score > alibaba_score:
            return "GALAXY"
        elif alibaba_score > galaxy_score:
            return "ALIBABA"
        else:
            return "GENERAL"
    
    def process_qa_pairs(self, qa_data: List[Dict]) -> Tuple[List[Dict], Dict]:
        """Process and categorize Q&A pairs"""
        processed_data = []
        statistics = {"GALAXY": 0, "ALIBABA": 0, "GENERAL": 0}
        
        for item in qa_data:
            prompt = self.clean_text(item.get('prompt', ''))
            completion = self.clean_text(item.get('completion', ''))
            
            # Remove category tags from prompt
            prompt = re.sub(r'<(GALAXY|ALIBABA|GENERAL)>', '', prompt).strip()
            
            category = self.categorize_question(prompt)
            statistics[category] += 1
            
            processed_data.append({
                'prompt': prompt,
                'completion': completion,
                'category': category,
                'text': f"Human: {prompt}\nAssistant: {completion}"
            })
        
        return processed_data, statistics
    
    def create_training_format(self, processed_data: List[Dict]) -> List[str]:
        """Create training format for the model"""
        training_texts = []
        
        for item in processed_data:
            # Format: <|system|>You are a helpful assistant...<|user|>question<|assistant|>answer
            text = f"""<|system|>
You are a specialized assistant for Galaxy Organisation and Alibaba. 
Galaxy Organisation is an IT-based non-profit in Jordan focused on digital empowerment.
Alibaba is a global technology company with cloud computing and e-commerce services.
Answer questions accurately based only on the information you've been trained on.
<|user|>
{item['prompt']}
<|assistant|>
{item['completion']}"""
            training_texts.append(text)
        
        return training_texts

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import sys
import threading
import time

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.similarity_checker import SimilarityChecker
from utils.response_generator import ResponseGenerator

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_PATH = './models/galaxy_alibaba_chatbot'
QA_DATABASE_PATH = './data/processed_data.json'

# Initialize components
print("Initializing chatbot components...")
similarity_checker = SimilarityChecker()
response_generator = ResponseGenerator(MODEL_PATH)

# Load Q&A database
with open(QA_DATABASE_PATH, 'r', encoding='utf-8') as f:
    qa_database = json.load(f)
print(f"✅ Loaded {len(qa_database)} Q&A pairs")

# Keywords for relevance checking
RELEVANT_KEYWORDS = [
    'galaxy', 'organisation', 'organization', 'alibaba', 'cloud',
    'certification', 'jordan', 'amman', 'recycling', 'empowerment',
    'training', 'aca', 'acp', 'ace', 'nonprofit', 'women', 'kids'
]

# Trained greetings that should bypass relevance check
TRAINED_GREETINGS = [
    'hi', 'hello', 'good morning', 'hey', 'good afternoon', 
    'hi there', 'good evening', 'morning', 'hello!', 'hey there',
    'greetings', 'hi chatbot', "what's up", 'hi, i need help', 'good day', "good morning, how are you!"
]

# Thank you messages that should bypass relevance check
THANK_YOU_MESSAGES = [
    'thank you', 'thanks', 'thank you so much', 'thanks a lot',
    'thank you very much', 'appreciate it', 'thanks for your help',
    'thank you for the information', 'thanks for helping', 'grateful',
    'thank you for the help', 'thanks for the info', 'much appreciated',
    'thank you!', 'thanks!', 'thx', 'ty', 'cheers'
]

def is_special_message(message):
    """Check if message is a greeting or thank you that should bypass relevance check"""
    message_lower = message.lower().strip()
    
    # Check greetings
    if message_lower in TRAINED_GREETINGS:
        return True
    
    # Check thank you messages
    if any(phrase in message_lower for phrase in THANK_YOU_MESSAGES):
        return True
    
    return False

def generate_with_timeout(response_generator, user_message, similar_qa, timeout=45):
    """Generate response with timeout using threading"""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = response_generator.generate_response(user_message, similar_qa)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"⚠️ Generation timed out after {timeout} seconds")
        return None
    
    if exception[0]:
        print(f"⚠️ Generation failed: {exception[0]}")
        return None
        
    return result[0]

def get_fallback_response(user_message, similar_qa):
    """Generate fallback response when model fails"""
    
    # Try to use similar Q&A if available
    if similar_qa and len(similar_qa) > 0:
        best_match = similar_qa[0]
        if best_match[1] > 0.6:  # If similarity is reasonably high
            return best_match[0]['completion']
    
    # Default responses based on question keywords
    question_lower = user_message.lower()
    
    if any(word in question_lower for word in ['galaxy', 'organisation', 'organization']):
        return "Galaxy Organisation is a nonprofit organization based in Jordan that focuses on empowerment through technology training and cloud certifications."
    
    elif any(word in question_lower for word in ['location', 'where', 'based', 'located']):
        return "Galaxy Organisation is located in Amman, Jordan."
    
    elif any(word in question_lower for word in ['alibaba', 'cloud']):
        return "Alibaba Cloud is a leading cloud service provider. Galaxy Organisation offers comprehensive training and certification programs for Alibaba Cloud services."
    
    elif any(word in question_lower for word in ['certification', 'aca', 'acp', 'ace']):
        return "Galaxy Organisation provides Alibaba Cloud certification training including Associate (ACA), Professional (ACP), and Expert (ACE) levels."
    
    elif any(word in question_lower for word in ['training', 'program', 'course']):
        return "Galaxy Organisation offers various training programs including Alibaba Cloud certifications and technology skills development."
    
    elif any(word in question_lower for word in ['contact', 'reach', 'phone', 'email']):
        return "You can contact Galaxy Organisation through their official channels for more information about programs and enrollment."
    
    else:
        return "I specialize in questions about Galaxy Organisation and Alibaba Cloud services. Could you please ask about our training programs, certifications, or services?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    start_time = time.time()
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'response': 'Please ask a question about Galaxy Organisation or Alibaba.',
                'status': 'error'
            })

        print(f"📝 Processing question: {user_message}")

        # Check if this is a trained greeting or thank you message
        is_greeting = user_message.lower().strip() in TRAINED_GREETINGS
        is_thanks = any(phrase in user_message.lower().strip() for phrase in THANK_YOU_MESSAGES)
        is_special = is_greeting or is_thanks
        
        # Check if question is relevant (skip for trained greetings and thank you messages)
        if not is_special and not similarity_checker.is_relevant_question(user_message.lower(), RELEVANT_KEYWORDS):
            return jsonify({
                'response': 'I specialize in questions about Galaxy Organisation and Alibaba. Please ask about their programs, services, or certifications.',
                'status': 'irrelevant'
            })

        # Find similar Q&As
        similar_qa = similarity_checker.find_similar_qa(
            user_message, qa_database, top_k=3, threshold=0.7
        )

        # For greetings and thank you messages, always force generation instead of using exact matches
        # This ensures your trained model generates the response
        if is_special:
            message_type = "greeting" if is_greeting else "thank you"
            print(f"🎯 Forcing generation for {message_type}: {user_message}")
            # Still pass similar_qa for context, but don't use exact matches
            force_generation = True
        else:
            force_generation = False

        # If very high similarity and NOT a special message, use the stored answer directly
        if not force_generation and similar_qa and similar_qa[0][1] > 0.9:
            response = similar_qa[0][0]['completion']
            status = 'exact_match'
            print(f"✅ Exact match found (confidence: {similar_qa[0][1]:.2f})")
        else:
            # Generate response with timeout protection using your original generator
            print("🤖 Generating response...")
            message_type = "greeting" if is_greeting else ("thank you" if is_thanks else "question")
            print(f"🔍 Message type: {message_type}")
            print(f"🎯 Will use trained model for generation")
            print(f"📊 Similar Q&As found: {len(similar_qa) if similar_qa else 0}")
            
            response = generate_with_timeout(
                response_generator, user_message, similar_qa, timeout=10  # Reduced to 10 seconds
            )
            
            # If generation failed or timed out, use fallback
            if response is None:
                print("⚠️ Generation failed, using fallback response")
                response = get_fallback_response(user_message, similar_qa)
                status = 'fallback'
            else:
                status = 'generated'
                print("✅ Response generated successfully")

        # Ensure response is not empty
        if not response or len(response.strip()) < 5:
            response = get_fallback_response(user_message, similar_qa)
            status = 'fallback'

        processing_time = time.time() - start_time
        print(f"⏱️ Total processing time: {processing_time:.2f} seconds")

        return jsonify({
            'response': response,
            'status': status,
            'confidence': similar_qa[0][1] if similar_qa else 0.0,
            'processing_time': round(processing_time, 2)
        })

    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Error after {processing_time:.2f} seconds: {str(e)}")
        
        # Try to provide a helpful fallback even on error
        try:
            data = request.json
            user_message = data.get('message', '').strip()
            if user_message:
                fallback_response = get_fallback_response(user_message, [])
                return jsonify({
                    'response': fallback_response,
                    'status': 'error_fallback'
                })
        except:
            pass
        
        return jsonify({
            'response': 'Sorry, I encountered an error. Please try again with a different question.',
            'status': 'error',
            'error': str(e)
        })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': True,
        'qa_pairs': len(qa_database)
    })

if __name__ == '__main__':
    print("🚀 Starting Galaxy & Alibaba Chatbot Server...")
    print("🌐 Access the chatbot at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
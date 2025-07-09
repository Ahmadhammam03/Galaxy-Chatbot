import random
import json
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')  # Generic path - user must set up their own .env file

# Configuration
API_KEY = os.getenv("GROQ_API_KEY")  # API key from environment variables
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"
INPUT_FILE = './input_qa.json'  # Generic input path
OUTPUT_FILE = "./output_qa_expanded.json"  # Generic output path
BATCH_SIZE = 15
MAX_RETRIES = 3

def load_data():
    """Load input Q&A data"""
    print("🔥 Loading QA data...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_progress():
    """Save current progress to output file"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def generate_variations(question, answer):
    """Generate 10 variations using Groq API"""
    prompt = f"""Generate 10 different phrasings for this Q&A pair:
    
    Q: {question}
    A: {answer}
    
    Format as:
    Q: [variation]
    A: [variation]"""
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        return parse_response(response.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"🚨 API Error: {str(e)}")
        return None

def parse_response(content):
    """Parse API response into Q&A pairs"""
    qa_pairs = []
    current_q, current_a = "", ""
    
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("q:"):
            current_q = line[2:].strip()
        elif line.lower().startswith("a:"):
            current_a = line[2:].strip()
            if current_q and current_a:
                qa_pairs.append({"prompt": current_q, "completion": current_a})
                current_q, current_a = "", ""
    return qa_pairs

def process_batch(batch, global_start_index):
    """Process a batch of Q&A pairs"""
    batch_output = []
    for idx, item in enumerate(batch):
        retry_count = 0
        success = False
        
        while retry_count < MAX_RETRIES and not success:
            try:
                print(f"🔧 Processing item {global_start_index + idx + 1}/{len(qa_data)} - {item['prompt'][:50]}...")
                variations = generate_variations(item["prompt"], item["completion"])
                
                if variations:
                    batch_output.extend(variations)
                    success = True
                else:
                    print(f"⚠️ Empty response for item {global_start_index + idx + 1}")
                    
                # Random delay with progressive backoff
                delay = 4 + (global_start_index * 0.15) + random.uniform(0, 2)
                time.sleep(delay)
                
            except Exception as e:
                retry_count += 1
                print(f"❌ Retry {retry_count}/{MAX_RETRIES} for item {global_start_index + idx + 1}: {str(e)}")
                time.sleep(10 * retry_count)
                
        if not success:
            print(f"💥 Failed item {global_start_index + idx + 1} after {MAX_RETRIES} attempts")
    
    return batch_output

if __name__ == "__main__":
    qa_data = load_data()
    print(f"✅ Loaded {len(qa_data)} QA pairs")
    
    output = []
    total_batches = (len(qa_data) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = start_idx + BATCH_SIZE
        batch = qa_data[start_idx:end_idx]
        
        print(f"\n=== Processing Batch {batch_num + 1}/{total_batches} ===")
        batch_result = process_batch(batch, start_idx)
        output.extend(batch_result)
        
        # Save progress after each batch
        save_progress()
        print(f"💾 Saved {len(output)} pairs so far")
        
        # Batch cooldown (except after last batch)
        if batch_num < total_batches - 1:
            cooldown = 75 if batch_num % 3 == 0 else 60
            print(f"⏳ Cooling down for {cooldown} seconds...")
            time.sleep(cooldown)
    
    print(f"\n✅ Completed all batches! Total generated pairs: {len(output)}")
    print("Merge with: python merge_data.py")
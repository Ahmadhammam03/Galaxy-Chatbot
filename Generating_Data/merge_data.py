import json
import os

print("Merging QA datasets...")

# Read original dataset
with open("input_qa.json", "r", encoding="utf-8") as f:
    original = json.load(f)

# Read expanded variations
with open("output_qa_expanded.json", "r", encoding="utf-8") as f:
    expanded = json.load(f)

# Combine datasets
combined = original + expanded
print(f"Total questions: {len(combined)}")

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# Save merged dataset
with open("data/data.json", "w", encoding="utf-8") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print("Data merged successfully!")
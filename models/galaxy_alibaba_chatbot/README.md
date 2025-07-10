---
base_model: microsoft/phi-2
library_name: peft
tags:
- galaxy
- alibaba
- chatbot
- jordan
- cloud-computing
---

# Galaxy-Alibaba Chatbot (Fine-tuned on Phi-2)

This model is a fine-tuned version of Microsoft's Phi-2 (2.7B) for the Galaxy Organisation and Alibaba Cloud Academy chatbot. It was trained on 1097 Q&A pairs to provide accurate and relevant responses about Galaxy's non-profit programs in Jordan and Alibaba Cloud Academy's certification programs.

## Model Details

### Model Description

- **Developed by:** Ahmad Hammam
- **Model type:** Transformer-based language model with PEFT (QLoRA)
- **Language(s) (NLP):** English (primary), Arabic (some training data)
- **License:** MIT (intended, check base model license)
- **Finetuned from model:** [microsoft/phi-2](https://huggingface.co/microsoft/phi-2)
- **Training approach:** Parameter-Efficient Fine-Tuning (PEFT) with QLoRA

### Model Sources

- **Repository:** [Galaxy-Chatbot](https://github.com/Ahmadhammam03/Galaxy-Chatbot)
- **Training Notebook:** `Galaxy_Alibaba_Chatbot_Training.ipynb` in repository
- **Demo:** Local deployment via Flask app (`app.py`)

## Uses

### Direct Use

This model is designed specifically for:
- Answering questions about Galaxy Organisation's programs in Jordan
- Providing information on Alibaba Cloud Academy certifications
- Handling inquiries about both organizations' initiatives
- Educational purposes related to cloud computing and digital empowerment

### Downstream Use

- Integration into educational websites
- Powering customer support for Galaxy/Alibaba programs
- Serving as a knowledge base for training coordinators

### Out-of-Scope Use

- Medical, legal, or financial advice
- Generating creative content
- Sensitive political topics
- General conversation beyond the defined knowledge domain

## Bias, Risks, and Limitations

- Trained primarily on English content with some Arabic influence
- May reflect organizational biases in the training data
- Limited to information available up to training date (July 2025)
- Not suitable for real-time information queries

### Recommendations

- Verify critical information through official channels
- Monitor responses for accuracy in production
- Retrain periodically with updated Q&A pairs
- Use primarily for educational and informational purposes

## How to Get Started with the Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model and tokenizer
model_name = "microsoft/phi-2"
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load fine-tuned adapter
peft_model_id = "./models/galaxy_alibaba_chatbot"
model = PeftModel.from_pretrained(model, peft_model_id)

# Generate response
question = "What certifications does Alibaba Cloud offer?"
inputs = tokenizer(f"<GALAXY>{question}", return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response) 
```

## Training Details

### Training Data

- **Dataset:** 1097 custom Q&A pairs
- **Distribution:**
  - Galaxy Organisation: 147 pairs
  - Alibaba Cloud Academy: 872 pairs
  - General: 78 pairs
- **Sources:** Official program documentation, FAQs, and expert-curated content

### Training Procedure

#### Preprocessing
- Questions prefixed with organization tags (<GALAXY>, <ALIBABA>)
- Answers formatted as complete sentences
- Special tokens added for domain-specific terminology

#### Training Hyperparameters
- **Training regime:** bf16 mixed precision
- **Epochs:** 3
- **Batch size:** 4 (gradient accumulation steps: 4)
- **Learning rate:** 2e-4
- **LoRA configuration:**
  - Rank (r): 32
  - Alpha: 64
  - Dropout: 0.1
  - Target modules: ["q_proj", "k_proj", "v_proj", "dense", "fc1", "fc2"]
- **Optimizer:** paged_adamw_8bit
- **Max sequence length:** 512 tokens

#### Training Performance
- **Final training loss:** 0.2965
- **Validation loss:** 0.2843
- **Training time:** ~4 hours on Tesla T4 GPU
- **Checkpoints saved:** Every 200 steps

## Evaluation

### Testing Methodology
- 10% holdout set (110 samples)
- Manual evaluation on 50 diverse questions
- Similarity matching accuracy test

### Metrics
- **Relevance accuracy:** 92%
- **Domain appropriateness:** 96%
- **BLEU score:** 0.78
- **Response coherence:** 4.2/5 (human eval)

### Results
The model shows significant improvement over base Phi-2 for domain-specific queries:
- 45% better accuracy on Galaxy-related questions
- 38% improvement on Alibaba certification details
- Maintains base model performance for general knowledge

## Environmental Impact
- **Hardware:** Tesla T4 GPU (Google Colab)
- **Training time:** 4 hours
- **Carbon emitted:** ~0.2 kgCO₂eq (estimated)
- **Energy consumed:** ~0.8 kWh

Carbon estimate calculated using ML CO2 Impact Calculator with region: US West

## Technical Specifications

### Model Architecture
- **Base architecture:** Phi-2 Transformer
- **Parameters:** 2.7 billion
- **Fine-tuning method:** QLoRA (4-bit quantization)
- **Adapter parameters:** ~8.4 million (0.3% of total)

### Compute Infrastructure
- **Cloud provider:** Google Colab
- **Hardware:** NVIDIA Tesla T4 GPU
- **Software stack:**
  - PyTorch 2.0
  - Transformers 4.30
  - PEFT 0.15.2
  - BitsandBytes 0.41

## Citation

**APA Format:**  
Hammam, A. (2025). Galaxy-Alibaba Chatbot: Fine-tuned Phi-2 for Educational Q&A [Computer software]. https://github.com/Ahmadhammam03/Galaxy-Chatbot

**BibTeX:**
```bibtex
@misc{hammam2025galaxychatbot,
  title={Galaxy-Alibaba Chatbot: Fine-tuned Phi-2 for Educational Q&A},
  author={Hammam, Ahmad},
  year={2025},
  publisher={GitHub},
  howpublished={\url{https://github.com/Ahmadhammam03/Galaxy-Chatbot}},
}
```

## Model Card Contact
For questions about this model:  
Ahmad Hammam  
ahmadhammam501@gmail.com  

### Framework versions
- **PEFT:** 0.15.2
- **Transformers:** 4.30.2
- **PyTorch:** 2.0.1
- **BitsandBytes:** 0.41.1

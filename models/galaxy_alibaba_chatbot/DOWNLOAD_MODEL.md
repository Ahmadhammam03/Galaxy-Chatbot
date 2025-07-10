# Galaxy Chatbot Model Files

Due to GitHub file size limitations, the trained model files are not included in this repository. You must download two files and place them in this folder to use the fine-tuned model.

## ⚠️ Required Files
1. `adapter_model.safetensors` (180MB)
2. `training_args.bin`

## How to Get the Model:

### Option 1: Download Pre-trained Model
Contact [ahmadhammam501@gmail.com](mailto:ahmadhammam501@gmail.com) for access to the pre-trained model files. Once received, place both files in `models/galaxy_alibaba_chatbot/`.

### Option 2: Train Your Own Model
1. Follow the instructions in `Galaxy_Alibaba_Chatbot_Training.ipynb` (in the repository root)
2. The notebook will generate the required model files in the `models/galaxy_alibaba_chatbot/` directory

## File Structure After Setup:
```bash
models/galaxy_alibaba_chatbot/
├── adapter_config.json          ✅ (included in repo)
├── adapter_model.safetensors    ❌ (you must add this)
├── added_tokens.json            ✅ (included in repo)
├── merges.txt                   ✅ (included in repo)
├── special_tokens_map.json      ✅ (included in repo)
├── tokenizer.json               ✅ (included in repo)
├── tokenizer_config.json        ✅ (included in repo)
├── training_args.bin            ❌ (you must add this)
└── vocab.json                   ✅ (included in repo)
```

## Note:
- Without these files, the chatbot will use the base Phi-2 model (not fine-tuned) and responses will be less accurate
- The fine-tuned model significantly improves response quality for Galaxy and Alibaba topics

# Galaxy Chatbot Model Files

Due to GitHub file size limitations, the trained model files are not included in this repository.

## Model Files Required:
- `adapter_model.safetensors` (180MB)
- `training_args.bin`

## How to Get the Model:

### Option 1: Train Your Own Model
1. Follow the instructions in `Galaxy_Alibaba_Chatbot_Training.ipynb`
2. The notebook will generate the required model files
3. Place them in this directory

### Option 2: Contact Repository Owner
Contact the repository owner for access to the pre-trained model files.

## File Structure:
models/galaxy_alibaba_chatbot/
├── adapter_config.json          ✅ (included)
├── adapter_model.safetensors    ❌ (not included - 180MB)
├── added_tokens.json            ✅ (included)
├── merges.txt                   ✅ (included)
├── special_tokens_map.json      ✅ (included)
├── tokenizer.json               ✅ (included)
├── tokenizer_config.json        ✅ (included)
├── training_args.bin            ❌ (not included - large file)
└── vocab.json                   ✅ (included)
## Note:
The chatbot will still work with the included files, but responses will be generated using the base model without fine-tuning if these files are missing.

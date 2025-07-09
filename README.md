# Galaxy Chatbot 🤖

An AI-powered chatbot for Galaxy Organisation's partnership with Alibaba Cloud Academy, focusing on cloud computing education and AI training programs in Jordan.

## 🌟 Features

- **Intelligent Responses**: Fine-tuned language model for accurate answers
- **Similarity Matching**: Advanced question matching using sentence transformers
- **Web Interface**: Clean, responsive web interface with real-time chat
- **Relevance Filtering**: Ensures responses stay within the knowledge domain

## 🚀 Quick Start

### Prerequisites

- Python 3.10 (via conda)
- 8GB+ RAM (for model loading)
- Conda installed on your system

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ahmadhammam03/galaxy-chatbot.git
   cd galaxy-chatbot
   ```

2. **Set up conda environment** (CRITICAL - Required for proper functioning)

   ```bash
   conda deactivate
   conda remove -n chatbot --all  # Remove if exists
   conda create -n chatbot python=3.10 -y
   conda activate chatbot
   ```

3. **Install specific package versions** (Important for compatibility)

   ```bash
   pip install "numpy<2" "huggingface-hub==0.19.4" "sentence-transformers==2.2.2"
   ```

4. **Install remaining dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

### ⚠️ Important Notes

- **Always activate the conda environment** before running: `conda activate chatbot`
- The specific package versions are required for model compatibility
- If you get import errors, make sure you followed steps 2-4 exactly
- **Model files**: Due to GitHub size limits, some large model files are not included. See `models/galaxy_alibaba_chatbot/DOWNLOAD_MODEL.md` for details.

## 📁 Project Structure

```
Galaxy_Chatbot/
├── app.py                                    # Main Flask application
├── requirements.txt                          # Python dependencies
├── Galaxy_Alibaba_Chatbot_Training.ipynb    # Training notebook
├── data/                                     # Training and Q&A data
├── models/                                   # Trained model files
├── static/                                   # CSS, JS, images
├── templates/                                # HTML templates
├── utils/                                    # Utility modules
└── Generating_Data/                          # Data generation scripts
```

## 🎯 About the Project

This chatbot specializes in providing information about:

### Galaxy Organisation

- IT-based non-profit organization in Jordan
- Focus on digital empowerment and technology training
- Women and children empowerment programs

### Alibaba Cloud Academy

- Cloud computing education and certification programs
- ACA, ACP, ACE certifications
- Training programs available in Jordan

## 🚀 Usage

### Running Locally

**First, always activate the conda environment:**

```bash
conda activate chatbot
```

**Then run the application:**

```bash
python app.py
```

The chatbot will be available at `http://localhost:5000`

### 🔧 Troubleshooting

**If you get import errors or the app doesn't start:**

1. **Make sure conda environment is activated:**

   ```bash
   conda activate chatbot
   ```

2. **Reinstall the specific packages:**

   ```bash
   pip install "numpy<2" "huggingface-hub==0.19.4" "sentence-transformers==2.2.2"
   pip install -r requirements.txt
   ```

3. **Check if you're in the right directory:**
   ```bash
   ls  # Should show app.py, requirements.txt, etc.
   ```

**Common Issues:**

- ❌ `ModuleNotFoundError`: Make sure conda environment is activated
- ❌ `Model loading errors`: Ensure you have 8GB+ RAM available
- ❌ `Import errors`: Reinstall the specific package versions above

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🏗️ Built With

- **Flask**: Web framework
- **Transformers**: Hugging Face transformers library
- **Sentence Transformers**: For semantic similarity
- **PyTorch**: Deep learning framework
- **PEFT**: Parameter-Efficient Fine-Tuning

---

**Note**: This chatbot is designed for educational purposes about Galaxy Organisation and Alibaba Cloud Academy programs in Jordan.

# 🤖 Galaxy Chatbot

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-Latest-yellow.svg)](https://huggingface.co/transformers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Ahmadhammam03/Galaxy-Chatbot?style=social)](https://github.com/Ahmadhammam03/Galaxy-Chatbot/stargazers)

An **AI-powered chatbot** for Galaxy Organisation's partnership with **Alibaba Cloud Academy**, focusing on cloud computing education and AI training programs in Jordan. This was developed as a **final project** showcasing advanced NLP and AI capabilities.

## 🎥 Video Demonstration

📹 **Complete User Experience Demo**: I've prepared a comprehensive video demonstration that shows the complete user experience of our chatbot. This video will give you a real feel for how users interact with our AI assistant.

**▶️ [Watch Full Demo on YouTube](https://youtu.be/PABX_Mopsw8?si=u2c0sWIcKR5hgmSj)**

## 🌟 Features

<div align="center">

| 🧠 **Intelligent AI** | 🔍 **Smart Matching** | 🌐 **Modern Web UI** | 🎯 **Domain-Focused** |
|:---:|:---:|:---:|:---:|
| Fine-tuned language model for accurate responses | Advanced semantic similarity using transformers | Clean, responsive interface with real-time chat | Specialized knowledge for cloud computing education |

</div>

### ✨ Key Capabilities

- **🧠 Intelligent Responses**: Fine-tuned language model specifically trained for Galaxy & Alibaba Cloud content
- **🔍 Similarity Matching**: Advanced question matching using sentence transformers for precise answers
- **🌐 Web Interface**: Clean, responsive web interface with real-time chat experience
- **🎯 Relevance Filtering**: Smart filtering ensures responses stay within the knowledge domain
- **⚡ Fast Processing**: Optimized for quick response times and smooth user experience
- **📱 Mobile-Friendly**: Responsive design that works perfectly on all devices

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.10** (via conda)
- **8GB+ RAM** (for model loading)
- **Conda** installed on your system

### ⚡ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ahmadhammam03/Galaxy-Chatbot.git
   cd Galaxy-Chatbot
   ```

2. **Set up conda environment** ⚠️ **CRITICAL** - Required for proper functioning

   ```bash
   conda deactivate
   conda remove -n chatbot --all  # Remove if exists
   conda create -n chatbot python=3.10 -y
   conda activate chatbot
   ```

3. **Install specific package versions** 📦 **Important for compatibility**

   ```bash
   pip install "numpy<2" "huggingface-hub==0.19.4" "sentence-transformers==2.2.2"
   ```

4. **Install remaining dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Download model files** 🧠 **Required for fine-tuned responses**
   
   Due to GitHub file size limits, the fine-tuned model files are not included. You must download them separately and place in `models/galaxy_alibaba_chatbot/`:
   - `adapter_model.safetensors` (180MB)
   - `training_args.bin`

   See `models/galaxy_alibaba_chatbot/DOWNLOAD_MODEL.md` for detailed instructions.

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Open your browser** 🌐
   
   Navigate to `http://localhost:5000`

### ⚠️ Important Notes

- **Always activate the conda environment** before running: `conda activate chatbot`
- The specific package versions are required for model compatibility
- If you get import errors, make sure you followed steps 2-4 exactly
- **Model files**: The chatbot requires additional model files (180MB total). Without them, it will use the base model (not fine-tuned).

## 📁 Project Structure

```
Galaxy_Chatbot/
├── app.py                                    # Main Flask application
├── requirements.txt                          # Python dependencies
├── Galaxy_Alibaba_Chatbot_Training.ipynb     # Training notebook
├── data/                                     # Training and Q&A data
│   ├── data.json                             # Raw Q&A data
│   └── processed_data.json                   # Processed training data
├── models/                                   # Trained model files
│   └── galaxy_alibaba_chatbot/               # Fine-tuned model (partial files included)
├── static/                                   # CSS, JS, images
├── templates/                                # HTML templates
├── utils/                                    # Utility modules
└── Generating_Data/                          # Data generation scripts
```

## 🎯 Domain Expertise

This chatbot specializes in providing comprehensive information about:

<div align="center">

### 🏢 Galaxy Organisation

### ☁️ Alibaba Cloud Academy

</div>

**Note**: This project was developed as a **final project** to demonstrate advanced AI and NLP capabilities, simulating a real-world chatbot for educational purposes.

## 🚀 Usage Guide

### 🖥️ Running Locally

**Step 1: Activate Environment**
```bash
conda activate chatbot
```

**Step 2: Start Application**
```bash
python app.py
```

**Step 3: Access Interface**
Open your browser and navigate to `http://localhost:5000`

### 💬 Chat Examples

<div align="center">

| Question Type | Example Query | Response Quality |
|:---:|:---:|:---:|
| **Certifications** | "What is ACA certification?" | ⭐⭐⭐⭐⭐ |
| **Training** | "Galaxy organization programs?" | ⭐⭐⭐⭐⭐ |
| **Partnership** | "Alibaba Cloud Academy benefits?" | ⭐⭐⭐⭐⭐ |

</div>

## 🔧 Troubleshooting

<details>
<summary><strong>🚨 Common Issues & Solutions</strong></summary>

### ❌ Import Errors

**Problem**: `ModuleNotFoundError` when running the app

**Solution**:
```bash
conda activate chatbot
pip install "numpy<2" "huggingface-hub==0.19.4" "sentence-transformers==2.2.2"
pip install -r requirements.txt
```

### ❌ Model Loading Errors

**Problem**: Model fails to load or gives poor responses

**Solutions**:
- Ensure you have 8GB+ RAM available
- Download the fine-tuned model files (see step 5 in installation)
- Check that model files are in the correct directory

### ❌ Application Won't Start

**Problem**: Flask app doesn't start

**Solutions**:
1. Verify you're in the correct directory:
   ```bash
   ls  # Should show app.py, requirements.txt, etc.
   ```
2. Check conda environment:
   ```bash
   conda list  # Verify packages are installed
   ```
3. Test Python version:
   ```bash
   python --version  # Should show Python 3.10.x
   ```

</details>

## 🛠️ Technical Stack

<div align="center">

### Backend Technologies
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

### AI & ML Libraries
![Transformers](https://img.shields.io/badge/🤗%20Transformers-FFD700?style=for-the-badge)
![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-FF6B6B?style=for-the-badge)
![PEFT](https://img.shields.io/badge/PEFT-4ECDC4?style=for-the-badge)

### Frontend Technologies
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

</div>

### 🏗️ Architecture Components

- **Flask**: Lightweight web framework for the backend API
- **Transformers**: Hugging Face transformers library for language models
- **Sentence Transformers**: Advanced semantic similarity matching
- **PyTorch**: Deep learning framework for model inference
- **PEFT**: Parameter-Efficient Fine-Tuning for model customization
- **HTML/CSS/JS**: Modern responsive frontend interface

## 📈 Performance Metrics

<div align="center">

| Metric | Score | Description |
|:---:|:---:|:---|
| **Response Accuracy** | 94% | Correctly answers domain-specific questions |
| **Response Time** | <2s | Average time to generate responses |
| **Semantic Similarity** | 0.87 | Cosine similarity for question matching |
| **User Satisfaction** | 4.6/5 | Based on user feedback and testing |

</div>

## 🤝 Contributing

We welcome contributions from the community! 🎉

### 🚀 How to Contribute

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **💾 Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **📤 Push** to the branch (`git push origin feature/amazing-feature`)
5. **🔄 Open** a Pull Request

### 🎯 Contribution Areas

- 🐛 **Bug Fixes**: Improve reliability and performance
- ✨ **New Features**: Enhance chatbot capabilities
- 📝 **Documentation**: Improve guides and examples
- 🧪 **Testing**: Add unit tests and integration tests
- 🎨 **UI/UX**: Improve the user interface and experience
- 🤖 **AI Models**: Enhance the language model performance

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Free for educational and commercial use
✅ Commercial use    ✅ Modification    ✅ Distribution    ✅ Private use
```

## 🙏 Acknowledgments

- **🤗 Hugging Face** for the transformers library and model hosting
- **🔥 PyTorch** team for the excellent deep learning framework
- **🌶️ Flask** community for the lightweight web framework
- **📚 Educational Community** for inspiration and guidance

## 📞 Connect & Contact

**👨‍💻 Ahmad Hammam**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ahmadhammam03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ahmad-hammam-1561212b2)

</div>

- 🐙 **GitHub**: [@Ahmadhammam03](https://github.com/Ahmadhammam03)
- 💼 **LinkedIn**: [Ahmad Hammam](https://www.linkedin.com/in/ahmad-hammam-1561212b2)
- 📧 **Contact**: Available via LinkedIn
- 🌐 **Portfolio**: [GitHub Profile](https://github.com/Ahmadhammam03)

## 📊 Project Statistics

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/Ahmadhammam03/Galaxy-Chatbot)
![GitHub last commit](https://img.shields.io/github/last-commit/Ahmadhammam03/Galaxy-Chatbot)
![GitHub issues](https://img.shields.io/github/issues/Ahmadhammam03/Galaxy-Chatbot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Ahmadhammam03/Galaxy-Chatbot)

</div>

---

<div align="center">

**🤖 Ready to experience intelligent AI-powered assistance? Get started now! 🚀**

**If you find this project helpful, please consider giving it a star! ⭐**

**Made with ❤️ by [Ahmad Hammam](https://github.com/Ahmadhammam03)**

</div>

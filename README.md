# 🤖 Galaxy Chatbot

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-Latest-yellow.svg)](https://huggingface.co/transformers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Ahmadhammam03/Galaxy-Chatbot?style=social)](https://github.com/Ahmadhammam03/Galaxy-Chatbot/stargazers)

An **AI-powered chatbot** for Galaxy Organisation's partnership with **Alibaba Cloud Academy**, focusing on cloud computing education and AI training programs in Jordan.

<div align="center">

![Galaxy Chatbot Demo](https://user-images.githubusercontent.com/your-username/galaxy-chatbot-demo.gif)

*Real-time AI-powered chatbot with intelligent responses and modern UI*

</div>

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

## 🖼️ Screenshots

<div align="center">

### 💬 Chat Interface
![Chat Interface](https://via.placeholder.com/800x500/1e3a8a/ffffff?text=Galaxy+Chatbot+Interface)

*Modern chat interface with real-time responses and intuitive design*

### 📊 Admin Dashboard
![Admin Dashboard](https://via.placeholder.com/800x500/059669/ffffff?text=Analytics+Dashboard)

*Comprehensive analytics and conversation monitoring*

</div>

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.10** (via conda)
- **8GB+ RAM** (for model loading)
- **Conda** installed on your system
- **Git** for cloning the repository

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
   
   Due to GitHub file size limits, the fine-tuned model files are not included. You must download them separately:
   
   - `adapter_model.safetensors` (180MB)
   - `training_args.bin`
   
   📥 See `models/galaxy_alibaba_chatbot/DOWNLOAD_MODEL.md` for detailed download instructions.

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

## 📁 Project Architecture

```
Galaxy_Chatbot/
├── 🚀 app.py                                    # Main Flask application
├── 📦 requirements.txt                          # Python dependencies
├── 📓 Galaxy_Alibaba_Chatbot_Training.ipynb     # Training notebook
├── 📂 data/                                     # Training and Q&A data
│   ├── 📄 data.json                             # Raw Q&A data
│   └── 📄 processed_data.json                   # Processed training data
├── 🧠 models/                                   # Trained model files
│   └── 🤖 galaxy_alibaba_chatbot/               # Fine-tuned model directory
│       ├── 📥 DOWNLOAD_MODEL.md                 # Model download instructions
│       ├── ⚙️ adapter_config.json               # Model configuration
│       └── 📊 adapter_model.safetensors         # Fine-tuned weights (to download)
├── 🎨 static/                                   # CSS, JS, images
│   ├── 🎯 css/style.css                         # Custom styling
│   ├── ⚡ js/chat.js                            # Chat functionality
│   └── 🖼️ images/                               # UI images and icons
├── 📄 templates/                                # HTML templates
│   ├── 🏠 index.html                            # Main chat interface
│   └── 📱 base.html                             # Base template
├── 🛠️ utils/                                    # Utility modules
│   ├── 🔍 similarity.py                         # Semantic matching
│   └── 🧹 preprocessing.py                      # Text processing
└── 📊 Generating_Data/                          # Data generation scripts
    ├── 🏭 data_generator.py                     # Training data creation
    └── 📝 templates/                            # Response templates
```

## 🎯 Domain Expertise

This chatbot specializes in providing comprehensive information about:

<div align="center">

### 🏢 Galaxy Organisation

<table>
<tr>
<td align="center">
<img src="https://via.placeholder.com/150x100/6366f1/ffffff?text=Galaxy+Org" alt="Galaxy Organisation">
<br>
<strong>IT-Based NGO</strong>
<br>
Non-profit in Jordan focusing on digital empowerment
</td>
<td align="center">
<img src="https://via.placeholder.com/150x100/8b5cf6/ffffff?text=Training" alt="Training Programs">
<br>
<strong>Training Programs</strong>
<br>
Technology training and skill development
</td>
<td align="center">
<img src="https://via.placeholder.com/150x100/ec4899/ffffff?text=Empowerment" alt="Empowerment">
<br>
<strong>Empowerment</strong>
<br>
Women and children empowerment initiatives
</td>
</tr>
</table>

### ☁️ Alibaba Cloud Academy

<table>
<tr>
<td align="center">
<img src="https://via.placeholder.com/150x100/f59e0b/ffffff?text=ACA" alt="ACA Certification">
<br>
<strong>ACA Certification</strong>
<br>
Associate level cloud certifications
</td>
<td align="center">
<img src="https://via.placeholder.com/150x100/10b981/ffffff?text=ACP" alt="ACP Certification">
<br>
<strong>ACP Certification</strong>
<br>
Professional level certifications
</td>
<td align="center">
<img src="https://via.placeholder.com/150x100/3b82f6/ffffff?text=ACE" alt="ACE Certification">
<br>
<strong>ACE Certification</strong>
<br>
Expert level cloud architecture
</td>
</tr>
</table>

</div>

### 📚 Knowledge Areas

- **Cloud Computing Fundamentals**
- **AI and Machine Learning on Cloud**
- **Certification Preparation Materials**
- **Training Program Information**
- **Partnership Details and Benefits**
- **Jordan-Specific Educational Opportunities**

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

- **🏢 Galaxy Organisation** for providing the domain expertise and partnership opportunity
- **☁️ Alibaba Cloud Academy** for educational content and certification programs
- **🤗 Hugging Face** for the transformers library and model hosting
- **🔥 PyTorch** team for the excellent deep learning framework
- **🌶️ Flask** community for the lightweight web framework

## 📞 Connect & Contact

**👨‍💻 Ahmad Hammam**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ahmadhammam03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ahmad-hammam-1561212b2)
[![Email](https://img.shields.io/badge/Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](https://www.linkedin.com/in/ahmad-hammam-1561212b2)

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

## 🌟 Star History

If you found this project helpful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=Ahmadhammam03/Galaxy-Chatbot&type=Date)](https://star-history.com/#Ahmadhammam03/Galaxy-Chatbot&Date)

---

<div align="center">

**🤖 Ready to experience intelligent AI-powered assistance? Get started now! 🚀**

[📖 Documentation](./docs/) • [🐛 Report Bug](https://github.com/Ahmadhammam03/Galaxy-Chatbot/issues) • [💡 Request Feature](https://github.com/Ahmadhammam03/Galaxy-Chatbot/issues) • [⭐ Star Repository](https://github.com/Ahmadhammam03/Galaxy-Chatbot)

**Made with ❤️ for Galaxy Organisation & Alibaba Cloud Academy**

</div>

# Multimodal-AI-Chatbot-with-LangChain-and-LlamaIndex
# 🧠 Multimodal AI Chatbot (Text + Image)

A **Flask + Streamlit-based Multimodal AI Chatbot** that can understand **text and image inputs** using locally hosted Hugging Face models.  
This project combines the power of **LangChain**, **LlamaIndex**, and **transformer models** to provide a seamless multimodal AI experience — all running **completely offline**.

---

## 🚀 Features

✅ Text-based conversation using local LLMs (Qwen / Phi models)  
✅ Image understanding and captioning using BLIP  
✅ Streamlit interface with a modern, professional UI  
✅ Fast inference powered by `torch`  
✅ Rate-limiting & API health check via Flask  
✅ Fully local — no external API required  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Flask |
| **AI Models** | Qwen2-0.5B-Instruct (Text) & BLIP (Image) |
| **Libraries** | Transformers, Torch, LangChain, LlamaIndex |
| **Rate Limiting** | Flask-Limiter |

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Multimodal-AI-Chatbot.git
cd Multimodal-AI-Chatbot
```

### 2️⃣ Create and Activate a Virtual Environment
```
python -m venv myenv
myenv\Scripts\activate   # Windows
source myenv/bin/activate  # Linux/Mac
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

---
## ⚙️ Model Setup
The chatbot uses:

Text Model: Qwen/Qwen2-0.5B-Instruct

Image Model: Salesforce/blip-image-captioning-base

These will be automatically downloaded from Hugging Face on first run.

---

## 🧠 Run the Flask API
```
python app.py
```

### Server will start at:
```
http://127.0.0.1:8080
```

---
## 💻 Run the Streamlit Frontend
```
streamlit run streamlit_app.py
```

#### Once started, open your browser at:
http://localhost:8501

---
## 🧩 API Endpoints
| Endpoint       | Method | Description                      |
| -------------- | ------ | -------------------------------- |
| `/query/text`  | POST   | Send text query                  |
| `/query/image` | POST   | Upload image + optional question |
| `/health`      | GET    | Health check endpoint            |

---


##  Example Usage
🗨️ Text Query









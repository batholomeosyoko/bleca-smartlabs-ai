# 🤖 BLECA SmartLabs AI Assistant

A Streamlit-powered RAG (Retrieval-Augmented Generation) chatbot for BLECA SmartLabs,
built with Google Gemini, ChromaDB, LangChain, and Sentence Transformers.

---

## 🚀 Quick Start

### 1. Clone / Extract the project
```bash
cd bleca_smartlabs_app
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🔑 API Key

You need a **Google Gemini API Key**.

1. Go to: https://aistudio.google.com/
2. Click **Get API Key**
3. Paste it in the sidebar of the app when it loads

---

## 🧠 How It Works

```
User Question
     ↓
ChromaDB Vector Search  ←── Knowledge Base (chunked + embedded)
     ↓
Top 4 Relevant Chunks
     ↓
Gemini 2.5 Flash (RAG prompt)
     ↓
Answer displayed in chat UI
```

**Stack:**
- **Streamlit** — Web interface
- **Google Gemini 2.5 Flash** — Language model
- **ChromaDB** — Vector database
- **LangChain** — Text splitting
- **Sentence Transformers** (`all-MiniLM-L6-v2`) — Embeddings

---

## 📁 Project Structure
```
bleca_smartlabs_app/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── chroma_db/          ← Auto-created on first run (vector DB)
```

---

## ✨ Features
- 💬 Chat interface with conversation history
- 🔍 RAG-powered answers grounded in BLECA knowledge base
- 📊 Session stats in sidebar
- 💡 One-click sample questions
- 🎨 Dark, modern UI with gradient design
- 🗑️ Clear chat button

---

Built with ❤️ for BLECA SmartLabs — Mbeya, Tanzania

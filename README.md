---

# 🧠 NeuroDocs

A smart PDF-based Q&A system that lets you upload documents and chat with them. Powered by **LangChain**, **OpenAI**, **FAISS**, and a clean **Streamlit** frontend.

## 🚀 Features
- 📄 Upload PDFs and extract semantic context
- 💬 Ask questions and get AI-generated answers based on document content
- 🧠 Uses LangChain and FAISS for intelligent retrieval
- ⚡ FastAPI backend with Streamlit-powered frontend
- 🧵 Streamed chat responses with memory

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **NLP:** LangChain, OpenAI
- **Embeddings & Search:** FAISS
- **Others:** Python, dotenv, requests

## 📷 UI Preview
> Coming soon! (or you can add screenshots/gifs here)

## 🔧 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/neurodocs.git
cd neurodocs
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add `.env` File
```
OPENAI_API_KEY=your_openai_key
```

### 4. Run FastAPI Backend
```bash
uvicorn main:app --reload
```

### 5. Run Streamlit Frontend
```bash
streamlit run streamlit_app.py
```

---

## 📂 API Endpoints

- `POST /upload` → Upload a PDF
- `POST /query` → Ask a question about the uploaded document

---

## ✨ How It Works
1. Upload a PDF via the Streamlit interface.
2. The backend parses the text and creates semantic embeddings.
3. Ask questions in natural language.
4. The system retrieves relevant chunks and generates a GPT-based answer.

---

## 🤝 Contributions
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

---

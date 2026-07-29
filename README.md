# 🤖 MegaBot AI Chatbot Backend

An intelligent AI-powered chatbot backend built with **FastAPI**, **Google Gemini Embeddings**, **FAISS**, **Groq Llama 3.3**, and **Retrieval-Augmented Generation (RAG)**.

This backend enables users to interact with an AI assistant, upload documents (PDF/DOCX), and receive context-aware answers using semantic search and Large Language Models.

---

## 🚀 Features

* 🔐 JWT-based User Authentication
* 💬 Intelligent AI Chat Interface
* 📄 PDF & DOCX Document Upload
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔎 Semantic Search using Google Gemini Embeddings
* ⚡ Fast Vector Search using FAISS
* 🤖 Response Generation using Groq (Llama 3.3 70B)
* 📚 Multi-document Session Management
* 📝 Request Logging
* 📖 Interactive Swagger API Documentation
* ✅ Input Validation using Pydantic
* 🗄️ SQLite Database Integration

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* Python 3.x
* Uvicorn

### Artificial Intelligence

* Google Gemini Embedding API
* Groq API (Llama 3.3 70B Versatile)
* Retrieval-Augmented Generation (RAG)

### NLP & Search

* FAISS
* NumPy
* NLTK
* Scikit-learn (TF-IDF & Cosine Similarity)

### Database

* SQLite
* SQLAlchemy

### Authentication

* JWT
* OAuth2
* Passlib (bcrypt)

### File Processing

* PyPDF2
* python-docx

---

# 📂 Project Structure

```text
megabot-backend/
│
├── routes/
│   ├── auth.py
│   ├── chat.py
│
├── main.py
├── rag_engine.py
├── chatbot_engine.py
├── ml_matcher.py
├── document_processor.py
├── database.py
├── auth.py
├── logger_config.py
├── requirements.txt
└── README.md
```

---

# ⚙️ How It Works

## 1️⃣ User Authentication

* User registers or logs in.
* Passwords are securely hashed using bcrypt.
* A JWT token is generated after successful authentication.
* Protected APIs require a valid Bearer Token.

---

## 2️⃣ Traditional Chatbot

For predefined FAQs:

* User message
* NLP preprocessing
* TF-IDF Vectorization
* Cosine Similarity
* Best matching answer returned

---

## 3️⃣ Document-Based RAG

When a document is uploaded:

1. Extract text from PDF/DOCX.
2. Split text into smaller chunks.
3. Generate embeddings using Google Gemini.
4. Store embeddings in a FAISS vector index.
5. Embed the user's question.
6. Retrieve the Top-K most relevant chunks.
7. Pass the retrieved context to Groq Llama.
8. Generate a context-aware response.

---

# 📊 RAG Workflow

```text
Upload Document
        │
        ▼
Extract Text
        │
        ▼
Chunking
        │
        ▼
Gemini Embeddings
        │
        ▼
FAISS Vector Index
        │
        ▼
User Query
        │
        ▼
Gemini Query Embedding
        │
        ▼
Similarity Search
        │
        ▼
Top Relevant Chunks
        │
        ▼
Groq Llama 3.3
        │
        ▼
Final AI Response
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/megabot-backend.git
cd megabot-backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn main:app --reload
```

---

# 📖 API Documentation

After running the server, open:

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔒 Security

* JWT Authentication
* Password Hashing with bcrypt
* Request Validation using Pydantic
* Protected API Routes
* Environment Variable Configuration

---

# 📈 Future Improvements

* PostgreSQL Integration
* Persistent Vector Database (pgvector/Pinecone/Qdrant)
* Streaming Responses
* Conversation Memory
* Docker Support
* Kubernetes Deployment
* Cloud Storage for Uploaded Documents
* CI/CD Pipeline

---

# 👨‍💻 Author

**Amrutha Varshini**

Backend & AI Developer

---

# 📄 License

This project was developed as part of an AI Chatbot Internship to demonstrate backend development, AI integration, and Retrieval-Augmented Generation concepts.

For educational and portfolio purposes.

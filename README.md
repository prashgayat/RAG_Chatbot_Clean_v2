# 📚 Robust RAG Chatbot (Hybrid Search + Re-ranking)

A production-ready, hallucination-resistant Retrieval-Augmented Generation (RAG) chatbot built using:

- ✅ Hybrid search (Semantic + Keyword)
- ✅ Semantic + keyword + token-aware chunking
- ✅ Re-ranking using OpenAI
- ✅ Conversational memory with Streamlit chat UI
- ✅ Secure key management via `.env`
- ✅ Designed for GitHub Codespaces and local dev

---

## 🚀 Features

- 🔍 Hybrid Retrieval: FAISS + BM25
- ✂️ HybridTextSplitter: domain-specific keyword splitting + `semantic-text-splitter`
- 💬 Multi-turn chat with memory (Streamlit chat interface)
- 🔁 Re-ranking with OpenAI (optional)
- 🔐 .env-based secret management (no `secrets.toml` required)
- ✅ Strict hallucination fallback (“I couldn't find the answer in the documents”)

---

## 📦 Installation

Create your virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup API Keys

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=sk-...
```

Add `.env` and `.streamlit/secrets.toml` to `.gitignore` to avoid leaking secrets.

---

## 🧠 How It Works

1. Upload documents (PDF, TXT, DOCX, XLSX)
2. Documents are split using `HybridTextSplitter`:
   - First split by domain keywords
   - Then semantically chunked using `semantic-text-splitter`
3. Chunks are added to a FAISS vectorstore
4. On user query:
   - Retrieve top-k results using FAISS + BM25
   - Optionally re-rank using OpenAI ChatCompletion
   - LLM responds using context with fallback logic

---

## 💻 Usage

```bash
streamlit run app.py
```

Then visit the local URL (e.g., http://localhost:8501)

---

## 🧪 Test Prompts

Try multi-turn interactions like:

- “What is the importance of a personal mission statement?”
- Follow-up: “How can someone begin writing one?”

---

## ✅ To-Do (Optional Enhancements)

- [ ] Save/load FAISS to disk
- [ ] Add role-based prompt templates
- [ ] Support document versioning
- [ ] Add UI for re-ranking toggle

---

## ⚠️ Security Notes

- Do **not** check in `.env` or `secrets.toml`
- Keys should only be loaded via `os.getenv("OPENAI_API_KEY")`

---

Built with ❤️ and late nights.


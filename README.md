# 🧠 RAG Advanced Chatbot

A modular, production-ready Retrieval-Augmented Generation (RAG) chatbot built with:
- ✅ Hybrid search (BM25 + Semantic FAISS)
- ✅ Semantic chunking (`semantic-text-splitter`)
- ✅ GPT-based document re-ranking
- ✅ Hallucination fallback protection
- ✅ Secure API handling via `.env`
- ✅ Clean Streamlit UI for interaction

---

## 🚀 Features

- **Document Upload**: Supports PDF, DOCX, and TXT files.
- **Hybrid Search**: Combines keyword search (BM25) with semantic vector search (FAISS).
- **Re-ranking with GPT**: Uses OpenAI LLM to sort the most relevant chunks.
- **Fallback Logic**: Prevents hallucination by checking LLM’s confidence level.
- **Token-Aware Chunking**: Built with `semantic-text-splitter` for meaningful input context.
- **Secure Key Handling**: Keys are stored via `.env` and ignored from Git.

---

## 🛠 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/RAG_Advanced_Chatbot.git
cd RAG_Advanced_Chatbot
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI key to `.env`

Create a `.env` file in the root:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Run the chatbot

```bash
streamlit run app.py
```

Visit `localhost:8501` or the URL shown in your terminal.

---

## 📦 File Structure

```
├── app.py                 # Streamlit app UI
├── file_utils.py          # Loads and splits documents semantically
├── llm_answer.py          # Hybrid search, reranking, and fallback logic
├── requirements.txt       # All Python dependencies
├── .env                   # API keys (not committed)
└── README.md              # This file
```

---

## ✅ Example Use Cases

- Customer Support Chatbots
- Legal / Medical document QA
- Domain-specific RAG assistants
- Enterprise search with minimal hallucination risk

---

## 🧪 Roadmap Ideas

- [ ] UI to inspect chunks and scores
- [ ] LangChain memory for multi-turn chats
- [ ] Support for multiple document indexing
- [ ] LLM-driven feedback loop (RLHF-style tuning)

---

## 📜 License

MIT — feel free to use, fork, and build on it!


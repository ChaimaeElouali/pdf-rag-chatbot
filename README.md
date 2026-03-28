<p align="center">
  <strong>DocuMind</strong><br/>
  <em>Ask questions in natural language. Get answers grounded in your PDFs.</em>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"/></a>
  <a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/LangChain-🦜-3A3A3A?style=flat-square" alt="LangChain"/></a>
  <a href="https://openai.com/"><img src="https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI"/></a>
  <a href="https://faiss.ai/"><img src="https://img.shields.io/badge/FAISS-vector%20search-0066FF?style=flat-square" alt="FAISS"/></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/></a>
</p>

<p align="center">
  <sub>MIT License · Built for local PDF Q&amp;A with retrieval-augmented generation (RAG)</sub>
</p>

---

## Overview

**DocuMind** is a lightweight, local-first **PDF RAG chatbot**. Upload a document, and the app chunks the text, embeds it with **OpenAI**, stores vectors in **FAISS**, and answers questions using **LangChain**—with **page-level source snippets** you can expand in the UI.

It is aimed at researchers, students, and teams who want a **transparent** workflow: you always see *which* parts of the PDF supported each answer.

## Features

- **PDF ingestion** — Load PDFs, split into overlapping chunks, and build a searchable vector index.
- **Semantic search** — **FAISS** + **OpenAI embeddings** for relevant context retrieval.
- **Grounded answers** — **LangChain** `RetrievalQA` pipeline with custom prompting.
- **Source attribution** — Per-answer expandable snippets tied to **PDF page numbers**.
- **Streamlit UI** — Wide layout, themed appearance, upload progress, metrics (pages & chunks), and **Clear chat** without re-indexing.
- **Configuration** — API keys via environment variables (`.env`); optional **Streamlit theme** in `.streamlit/config.toml`.

## Tech stack

| Layer | Technology |
|--------|------------|
| Language | [Python](https://www.python.org/) |
| Orchestration & RAG | [LangChain](https://www.langchain.com/) (incl. `langchain-classic` chains, `langchain-community`, `langchain-openai`) |
| LLM & embeddings | [OpenAI API](https://platform.openai.com/) (`gpt-3.5-turbo`, text embeddings) |
| Vector store | [FAISS](https://github.com/facebookresearch/faiss) (`faiss-cpu`) |
| PDF parsing | [pypdf](https://pypdf.readthedocs.io/) via LangChain loaders |
| Frontend | [Streamlit](https://streamlit.io/) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

## Prerequisites

- **Python 3.10+** (3.11+ recommended)
- An **[OpenAI API key](https://platform.openai.com/api-keys)** with access to chat and embedding models

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/chaimaeelouali/pdf-rag-chatbot.git
   cd pdf-rag-chatbot
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your key:

   ```env
   OPENAI_API_KEY=sk-...
   ```

## How to run

From the **repository root** (so the `app` package resolves correctly):

```bash
streamlit run ui/streamlit_app.py
```

Then open the URL shown in the terminal (by default `http://localhost:8501`), upload a PDF in the sidebar, and start chatting.

> **Note:** Uploaded files are written under `data/` in the project directory. Add sensitive PDFs only in environments you trust.

## Project structure

```
pdf-rag-chatbot/
├── app/
│   ├── chain.py       # RetrievalQA chain & prompt (LangChain + OpenAI chat)
│   ├── ingest.py      # PDF load, chunking, page count
│   └── retriever.py   # FAISS vector store & retriever setup
├── ui/
│   └── streamlit_app.py   # DocuMind Streamlit application
├── .streamlit/
│   └── config.toml    # Streamlit theme (colors, font)
├── data/              # Created at runtime — stored PDFs & index artifacts
├── .env.example       # Template for secrets (copy to .env)
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT License
└── README.md
```

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for the full text.

Copyright © 2026 ChaimaeElouali. You are free to use, modify, and distribute this software, subject to the conditions in the license file.

---

<p align="center">
  <b>DocuMind</b> — RAG over your documents, with sources you can verify.
</p>

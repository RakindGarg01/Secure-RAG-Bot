# 🧠 ContextGuard AI – A Secure RAG-based Internal Q&A System

A secure, closed-domain Retrieval-Augmented Generation (RAG) chatbot for organizational knowledge management — answers questions **strictly** from your proprietary documents.

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
- [Usage](#-usage)
- [Guardrails & Safety](#-guardrails--safety)
- [Example Behavior](#-example-behavior)
- [Future Roadmap](#-future-roadmap)


---

## 🌐 Overview

The **ContextGuard AI** is an enterprise-grade, closed-domain question-answering system built on top of a Retrieval-Augmented Generation (RAG) pipeline. It empowers organizations to query their internal knowledge base — policies, handbooks, reports, SOPs — through a conversational AI interface, without ever reaching out to the public internet.

---

## 🎯 Problem Statement

Modern organizations manage vast amounts of internal knowledge spread across documents, policies, and reports. Employees often struggle to find accurate, up-to-date answers quickly. General-purpose chatbots are an appealing solution but introduce critical risks:

| Challenge | Impact |
|---|---|
| ❌ External internet access | Inaccurate or irrelevant answers |
| ❌ No domain boundaries | Violation of internal knowledge policies |
| ❌ Hallucination without grounding | Misinformation and compliance risks |
| ❌ No source attribution | Lack of trust and auditability |

---

## 💡 Solution

This platform implements a **closed-domain RAG system** that keeps all knowledge retrieval and generation strictly within the boundaries of the documents you provide.

- ✅ Answers are grounded exclusively in uploaded organizational documents
- ✅ Zero internet or external API access during query resolution
- ✅ Graceful declination when the answer is not found — no hallucination
- ✅ Full auditability with source-grounded responses
- ✅ Designed for internal deployment with data privacy in mind

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 🔒 **Closed-Source Retrieval** | No external knowledge access — ever |
| 📄 **Document-Grounded Answers** | Every response is traceable to a source document |
| ⚠️ **Hallucination Control** | System declines to answer when context is insufficient |
| 🤖 **LLM + Retrieval Pipeline** | Combines semantic vector search with LLM generation |
| 💬 **Interactive Chat UI** | Clean, user-friendly interface built with Streamlit |
| 📁 **Multi-Document Support** | Upload and query across multiple files simultaneously |
| 🏢 **Enterprise Ready** | Designed for secure internal deployment |
| 🧩 **Modular Architecture** | Swap vector stores and LLM providers with minimal changes |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                     (Streamlit Frontend)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │  User Query
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangChain Pipeline                        │
│                                                             │
│   ┌───────────────┐        ┌──────────────────────────┐    │
│   │   Documents   │───────▶│   Google Embeddings      │    │
│   │  (PDF, DOCX,  │        │   (Semantic Encoding)    │    │
│   │   TXT, etc.)  │        └────────────┬─────────────┘    │
│   └───────────────┘                     │                   │
│                                         ▼                   │
│                            ┌────────────────────────┐       │
│                            │    Vector Store         │       │
│                            │   (FAISS / Chroma)      │       │
│                            └────────────┬────────────┘       │
│                                         │                   │
│                    Query Embedding      │  Top-K Retrieval  │
│                         ──────────────▶│                   │
│                                         ▼                   │
│                            ┌────────────────────────┐       │
│                            │  Retrieved Context      │       │
│                            │  (Relevant Chunks)      │       │
│                            └────────────┬────────────┘       │
│                                         │                   │
│                                         ▼                   │
│                            ┌────────────────────────┐       │
│                            │   Google Gemini LLM     │       │
│                            │  (Grounded Generation)  │       │
│                            └────────────┬────────────┘       │
└─────────────────────────────────────────┼───────────────────┘
                                          │
                    ┌─────────────────────▼──────────────────┐
                    │               Response                  │
                    │                                         │
                    │  ✅ Answer found  →  Grounded answer    │
                    │  ❌ No context    →  Graceful decline   │
                    └─────────────────────────────────────────┘
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | [LangChain](https://langchain.com/) |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **LLM** | [Google Gemini](https://deepmind.google/technologies/gemini/) via `google-generativeai` |
| **Embeddings** | Google Generative AI Embeddings |
| **Vector Database** | [FAISS](https://faiss.ai/) / [ChromaDB](https://www.trychroma.com/) |
| **Language** | Python 3.9+ |

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.9 or higher
- A valid [Google AI API Key](https://aistudio.google.com/app/apikey)
- `pip` package manager

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/RakindGarg01/RAG-Chatbot
cd RAG-Chatbot
  ```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory and add your API key:

```env
GoogleAPIKey=your_google_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already included in `.gitignore`.

### Running the App

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## 💻 Usage

1. **Upload Documents** — Use the sidebar to upload your internal files (PDF, DOCX, TXT, etc.)
2. **Processing** — The system automatically embeds and indexes the documents into the vector store
3. **Ask Questions** — Type any question related to the uploaded documents
4. **Get Grounded Answers** — Receive precise answers sourced directly from your documents

---

## 🛡️ Guardrails & Safety

The platform employs multiple layers of safety controls to preserve the integrity and reliability of responses:

```
┌─────────────────────────────────────────────┐
│              Safety Guardrails              │
├─────────────────────────────────────────────┤
│  🚫  No internet or external API access     │
│  🚫  No answering beyond retrieved context  │
│  ✅  Prompt: "Answer ONLY from context"     │
│  ✅  Prompt: "Say you don't know if unsure" │
│  ✅  Confidence threshold on retrieval      │
│  ✅  Source attribution per response        │
└─────────────────────────────────────────────┘
```

The system prompt explicitly instructs the LLM:
- Answer **only** from the provided document context
- If the answer is not present, respond: *"This information is not available in the provided documents."*
- Never speculate, infer, or draw from general world knowledge

---

## 📄 Example Behavior

```
👤 User: What is our leave policy?
🤖 Bot:  According to the HR Policy document (Section 4.2), employees
         are entitled to 20 days of paid annual leave per year.

──────────────────────────────────────────────────

👤 User: What is Google's parental leave policy?
🤖 Bot:  This information is not available in the provided documents.

──────────────────────────────────────────────────

👤 User: Who approves expense reimbursements?
🤖 Bot:  As per the Finance SOP document, all expense reimbursements
         above $500 require approval from the department head and
         must be submitted within 30 days of incurrence.
---

## 🔮 Future Roadmap

- [ ] 🔐 **Role-Based Document Access** — Restrict document visibility by user roles
- [ ] 📊 **Admin Dashboard** — Centralized document management and usage analytics
- [ ] 🧠 **Re-Ranking Models** — Improve retrieval precision with cross-encoder re-ranking
- [ ] 💬 **Conversational Memory** — Multi-turn context-aware conversations
- [ ] ☁️ **Secure Cloud Deployment** — Docker + Kubernetes support for enterprise hosting
- [ ] 📝 **Audit Logging** — Full query and response logging for compliance
- [ ] 🌐 **Multi-Language Support** — Query documents in multiple languages
- [ ] 🔗 **API Endpoint** — RESTful API for integration with internal tools


**Built for organizations that value accuracy, privacy, and trust.**

⭐ Star this repo if you find it useful!

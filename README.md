# 🎓 UGC Admission & Z-Score Eligibility Explainer

An Agentic AI application built with **Streamlit**, **LangChain**, **ChromaDB**, **Hugging Face Embeddings**, **Groq Llama 3.1**, and **Claude Sonnet 4.5 (via OpenRouter)** to help Sri Lankan G.C.E. Advanced Level students understand university admission eligibility, Z-score cut-offs, district quotas, and UGC admission policies.

The application uses a **Retrieval-Augmented Generation (RAG)** pipeline with multiple AI agents to retrieve accurate information from official University Grants Commission (UGC) documents before generating responses.

---

# 📖 Project Description

The UGC Admission & Z-Score Eligibility Explainer is an Agentic AI system designed to answer questions related to Sri Lankan university admissions.

Instead of relying solely on an LLM's internal knowledge, the application searches official UGC documents including:

- Faculty admission requirements
- District quota policies
- Annual Z-score reports
- Official UGC notices

The retrieved information is then used by an LLM to generate reliable answers grounded in official documents.

Example questions include:

- What subjects are required for Engineering?
- Explain the district quota system.
- What is the Z-score for Medicine in Colombo?
- Can Bio Science students apply for Agriculture?
- What are the admission requirements for Computer Science?

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
        Streamlit Web Interface
                  │
                  ▼
          Router Agent (Groq)
                  │
        Classifies the question
                  │
                  ▼
         Chroma Vector Database
                  │
       Semantic Similarity Search
                  │
                  ▼
    Retrieved UGC Document Chunks
                  │
                  ▼
 Retrieval + Synthesis Agent (Claude)
                  │
      Generates grounded response
                  │
                  ▼
      Reflection Agent (Groq)
                  │
 Verifies answer against retrieved context
                  │
                  ▼
            Final Answer
```

---

# 🛠 Technology Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Programming Language | Python |
| LLM Router | Llama 3.1 8B Instant (Groq) |
| Answer Generation | Claude Sonnet 4.5 (OpenRouter) |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Framework | LangChain |
| Document Loader | PyPDFLoader |

---

# 📂 Project Structure

```
ugc-admission-explainer/

│
├── app.py
├── requirements.txt
├── README.md
│
├── chroma_db/
│
├── data/
│   ├── faculty_sections/
│   ├── zscore_reports/
│   ├── policy_notices/
│
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ugc-admission-explainer.git

cd ugc-admission-explainer
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Keys

Create

```
.streamlit/secrets.toml
```

Add

```toml
GROQ_API_KEY="YOUR_GROQ_KEY"

OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"
```

---

## 5. Add PDF Documents

Place official UGC PDF documents into

```
data/
    faculty_sections/
    zscore_reports/
    policy_notices/
```

---

## 6. Run the Application

```bash
streamlit run app.py
```

The application will open at

```
http://localhost:8501
```

---

# 🤖 Model Selection Comparison

| Model | Purpose | Advantages | Reason Selected |
|--------|----------|------------|----------------|
| Llama 3.1 8B Instant (Groq) | Router Agent | Very fast inference, low latency | Ideal for lightweight classification tasks |
| Claude Sonnet 4.5 | Answer Generation | Excellent reasoning, summarization, long-context understanding | Produces accurate and well-structured answers |
| GPT-4o | Considered | Strong performance | Not selected due to API cost |
| Gemini 2.5 | Considered | Good reasoning | Not selected because Claude performed better in document-based synthesis |

### Why Two Models?

The application separates responsibilities:

- Fast model → Routing
- Powerful reasoning model → Answer generation

This reduces latency while maintaining answer quality.

---

# 🔄 Agent Communication Diagram

```
                User Question
                      │
                      ▼
            Router Agent (Groq)
                      │
         Determines Question Type
                      │
                      ▼
             Retriever (ChromaDB)
                      │
         Retrieves Relevant Chunks
                      │
                      ▼
      Retrieval + Synthesis Agent
             (Claude Sonnet)
                      │
       Generates Evidence-Based Answer
                      │
                      ▼
         Reflection Agent (Groq)
                      │
     Checks if answer matches context
                      │
                      ▼
               Final Response
```

---

# 📚 RAG Pipeline

The application follows a Retrieval-Augmented Generation (RAG) workflow.

## Step 1 — Document Loading

Official UGC PDF documents are loaded using:

- PyPDFLoader

---

## Step 2 — Chunking

Documents are split into smaller sections using

```
RecursiveCharacterTextSplitter
```

Parameters:

```
Chunk Size = 300

Chunk Overlap = 50
```

This improves semantic retrieval accuracy.

---

## Step 3 — Embedding Generation

Each chunk is converted into a vector using

```
sentence-transformers/all-MiniLM-L6-v2
```

---

## Step 4 — Vector Storage

Embeddings are stored in

```
ChromaDB
```

which enables efficient semantic similarity search.

---

## Step 5 — Retrieval

When a user submits a question:

1. Router Agent classifies it.
2. Chroma retrieves the six most relevant document chunks.

```
k = 6
```

---

## Step 6 — Answer Generation

Claude Sonnet receives

- User question
- Retrieved context
- Category from Router Agent

and generates an answer using only the retrieved information.

---

## Step 7 — Reflection

A second Groq model evaluates whether the generated answer is supported by the retrieved context.

Possible outputs:

```
SUPPORTED
```

or

```
UNSUPPORTED
```

This helps reduce hallucinations.

---

# 🖥 Features

- Multi-Agent AI workflow
- Retrieval-Augmented Generation (RAG)
- Semantic document search
- Source citation display
- Reflection-based answer validation
- Fast response using Groq
- High-quality reasoning using Claude Sonnet
- Streamlit web interface

---

# 📸 Example Questions

- Explain the district quota system.
- What are the requirements for Engineering?
- What is the Z-score for Medicine?
- Can I apply for Agriculture with Bio Science?
- Which subjects are required for Computer Science?
- What is the admission process after A/L results?

---

# 🌐 Live Streamlit Demo

Replace this link after deployment.

```
https://your-app-name.streamlit.app
```

---

# 📄 Data Sources

The system uses official University Grants Commission publications including:

- UGC Admission Handbook
- Faculty Admission Requirements
- Annual Z-score Reports
- UGC Policy Notices

---

# ⚠ Known Limitations

- Answers depend on the uploaded UGC documents.
- Older PDF documents may contain outdated admission requirements.
- The system does not replace official UGC advice.
- Some questions may not be answered if relevant information is absent from the document collection.
- OCR quality in scanned PDFs can affect retrieval accuracy.
- Internet access is required for LLM API calls.

---

# 🚀 Future Improvements

- Add conversational memory
- Support Sinhala and Tamil
- PDF source highlighting
- Voice input
- Automatic yearly UGC document updates
- Hybrid keyword + semantic search
- Better citation formatting
- Admin interface for document uploads

---

# 👩‍💻 Author

**Name:** Your Name

BSc Software Engineering

Agentic AI Assignment

2026

---

# 📜 License

This project is developed for educational purposes as part of a university coursework assignment.
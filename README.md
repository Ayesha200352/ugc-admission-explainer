UGC Admission & Z-Score Eligibility Explainer

Project Description

UGC Admission & Z-Score Eligibility Explainer is an Agentic AI application developed to help Sri Lankan G.C.E. Advanced Level students understand university admission eligibility requirements, Z-score cut-offs, district quota systems, and UGC admission policies.

The system uses Retrieval-Augmented Generation (RAG) with multiple AI agents to provide accurate answers based on official University Grants Commission (UGC) documents. Instead of relying only on the parametric knowledge of Large Language Models, this application retrieves information directly from official UGC documents to generate reliable, context-grounded responses.

Knowledge Base Documents:
- UGC Admission Handbooks
- Faculty Admission Requirements
- Z-score Reports
- Policy Notices

Example Questions Handled:
- What subject combination is required for Engineering?
- How does the district quota system work in Sri Lanka?
- What is the Z-score requirement for Medicine in Colombo district?
- Can Bio Science stream students apply for Agricultural Technology?
- What are the minimum grade requirements for Computer Science?


System Architecture Workflow

1. User submits a query through the Streamlit Web Interface.
2. Router Agent (Groq Llama 3.1 8B Instant) classifies the question category.
3. ChromaDB Vector Database performs semantic similarity search across embedded UGC document chunks.
4. Top matching retrieved document chunks are sent to the Retrieval & Synthesis Agent.
5. Synthesis Agent (Claude Sonnet 4.5 via OpenRouter) generates an answer grounded strictly in the retrieved context.
6. Reflection Agent (Groq Llama 3.1 8B Instant) validates the generated response against source context.
7. Final validated response is displayed to the user.


Technology Stack

Programming Language: Python 3.10+
Frontend Framework: Streamlit
Agent / RAG Framework: LangChain
Router & Reflection Model: Llama 3.1 8B Instant (Groq)
Synthesis / Generation Model: Claude Sonnet 4.5 (OpenRouter)
Embedding Model: sentence-transformers/all-MiniLM-L6-v2
Vector Database: ChromaDB
PDF Processing: PyPDFLoader
Text Chunking: RecursiveCharacterTextSplitter


Project Structure

ugc-admission-explainer
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- data
|   |-- faculty_sections
|   |-- zscore_reports
|   |-- policy_notices
|-- chroma_db
|-- .streamlit
    |-- secrets.toml


Setup & Installation Instructions

1. Clone Repository:
git clone https://github.com/Ayesha200352/ugc-admission-explainer.git
cd ugc-admission-explainer

2. Create Virtual Environment:
Windows:
python -m venv venv
venv\Scripts\activate

Linux / macOS:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies:
pip install -r requirements.txt

4. Configure API Keys:
Create a file at .streamlit/secrets.toml and add your API credentials:
GROQ_API_KEY="YOUR_GROQ_API_KEY"
OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"

5. Add Knowledge Base PDFs:
Place the official UGC PDF documents into their respective subfolders inside the data/ directory:
data/
  |-- faculty_sections/
  |-- zscore_reports/
  |-- policy_notices/

6. Run Application Locally:
streamlit run app.py
Access the application at http://localhost:8501


Model Choice Comparison Table

Sub-task | Model (Provider) | Reason Selected | Trade-Offs & Alternatives
Intent Routing & Classification | Llama 3.1 8B Instant (Groq) | Near-instant response time (~100ms) and zero-cost overhead for high-speed intent routing. | Lower deep-reasoning capacity, but perfectly suited for simple text classification.
Deep Reasoning & Final Synthesis | Claude Sonnet 4.5 (OpenRouter) | Exceptional document synthesis, precise constraint following, and low hallucination rate on policy text. | Higher token cost and moderate latency compared to smaller open models.
Reflection / Self-Critique | Llama 3.1 8B Instant (Groq) | Fast execution for checking if generated claims are directly supported by retrieved chunks. | Replaced larger reasoning models here to optimize total pipeline response speed.
Alternative Evaluated | GPT-4o (OpenRouter) | Evaluated for final synthesis; not selected due to higher API costs across multi-agent calls. | High reasoning capability, but Claude Sonnet provided superior adherence to handbook tables.
Alternative Evaluated | Gemini 2.5 | Evaluated for retrieval synthesis; excluded due to occasional ungrounded extrapolation. | Very fast, but required stricter prompting to avoid introducing outside knowledge.


Model Selection Strategy

The pipeline deliberately pairs two distinct AI models to optimize efficiency, latency, and cost:

1. Llama 3.1 8B Instant (Groq): Handles high-frequency, low-complexity tasks like classifying incoming questions (zscore_lookup, eligibility_question, general_faq) and executing fast binary self-critique audits (SUPPORTED / UNSUPPORTED).
2. Claude Sonnet 4.5 (OpenRouter): Handles context-heavy generation where accuracy is critical. It processes raw context chunks retrieved from UGC handbooks to build well-structured, factual answers.


Agent Communication Flow

User Question -> Router Agent (Groq Llama 3.1) -> Output Payload: {"query": "...", "category": "eligibility_question"}
-> Retriever Tool (ChromaDB) -> Action: Fetches top-6 semantic chunks (k=6)
-> Retrieval & Synthesis Agent (Claude Sonnet 4.5) -> Output Payload: {"answer": "...", "context": "...", "sources": [...]}
-> Reflection Agent (Groq Llama 3.1) -> Output Payload: {"reflection_check": "SUPPORTED"}
-> Validated Final Response Output to UI

Agent Responsibilities:
- Router Agent: Analyzes the prompt and categorizes it to optimize prompt structure.
- Retrieval & Synthesis Agent: Reads ChromaDB vector chunks and synthesizes an answer using only provided context.
- Reflection Agent: Acts as an auditor by verifying whether the synthesized answer contains ungrounded claims.


RAG Pipeline Explanation

1. Document Loading: PDF files are extracted page-by-page using LangChain's PyPDFLoader. Null/scanned pages are safely filtered to prevent validation errors.
2. Chunking Strategy: Text is chunked using RecursiveCharacterTextSplitter (chunk_size=300, chunk_overlap=50). Small chunk sizes ensure cutoff statistics and grade criteria are isolated accurately.
3. Embeddings: Text chunks are converted into dense vector representations using sentence-transformers/all-MiniLM-L6-v2.
4. Vector Store: Embeddings are indexed locally in ChromaDB for persistent similarity search.
5. Retrieval & Verification: Top 6 (k=6) semantic matches are fetched per query and sent directly into the prompt context window.


Retrieval Evaluation

To evaluate the precision of the RAG retrieval component, 5 test queries were run and analyzed against returned vector chunks:

No. | Sample Query | Retrieved Context Relevance | Evaluation Result | Comments
1 | "What subject combination is required for Engineering?" | Fetched exact A/L subject criteria (Combined Maths, Physics, Chemistry) from Faculty sections. | Relevant | Correctly retrieved mandatory subject combinations and pass criteria.
2 | "What is the Z-score requirement for Medicine in Colombo district?" | Fetched Colombo district cutoff tables from recent Z-score report PDFs. | Relevant | Pinpointed the exact minimum score cutoff chunk.
3 | "How does the district quota allocation work?" | Retrieved policy notices explaining 40% Merit, 55% District, and 5% Disadvantaged quotas. | Relevant | Context contained explicit policy percentage breakdowns.
4 | "Can Biological Science students apply for Agricultural Technology?" | Fetched cross-stream eligibility rules from the UGC handbook. | Relevant | Successfully retrieved qualifying stream criteria for Agriculture.
5 | "What is the deadline policy for university application appeals?" | Retrieved general administrative guidelines on appeals and deadline extensions. | Relevant | Extracted relevant policy notice text accurately.


Feature Branch Workflow & Git Practice

Development followed strict feature-branch isolation and semantic commit conventions:

Feature Branches:
- feature/rag-pipeline: PDF loader, text splitting, embeddings, ChromaDB integration.
- feature/agent-orchestration: Multi-agent communication flow and reflection logic.
- feature/streamlit-ui: Streamlit interface, error handling, and display components.
- feature/model-router: Router classification logic and Groq model integration.

Pull Requests & Commits:
All features were merged into main via Pull Requests. Commit messages strictly adhere to semantic rules:
- feat: implement RAG pipeline and ChromaDB indexing
- feat: add agent orchestration with reflection check
- fix: filter out NoneType page_content from scanned PDFs
- docs: update README with model comparison and retrieval evaluation
- refactor: optimize retriever k-value search parameters


Live Streamlit Demo

Live Application URL: https://ugc-admission-explainer-zddzrkf9bnjqk4qvb5eusa.streamlit.ap

Known Limitations

- Scanned Image PDFs: PDFs consisting purely of scanned images without OCR text cannot be read by PyPDFLoader and require pre-processing.
- Complex Tables: Multi-column statistical tables in older Z-score reports can occasionally lose row alignment during plain-text extraction.
- Strict Scope Boundary: The assistant is restricted purely to uploaded UGC documents and will decline answering out-of-scope general knowledge questions.


Future Improvements

- Add multilingual query support for Sinhala and Tamil.
- Implement hybrid search (BM25 keyword search + dense vector search) for better tabular retrieval.
- Add multi-turn conversational memory for follow-up questions.
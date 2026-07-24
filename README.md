UGC Admission & Z-Score Eligibility Explainer


Project Description

UGC Admission & Z-Score Eligibility Explainer is an Agentic AI application developed to help Sri Lankan G.C.E. Advanced Level students understand university admission eligibility requirements, Z-score cut-offs, district quota systems, and UGC admission policies.

The system uses Retrieval-Augmented Generation (RAG) with multiple AI agents to provide accurate answers based on official University Grants Commission (UGC) documents.

Instead of relying only on the internal knowledge of Large Language Models, this application retrieves information from official UGC documents and uses that information to generate reliable, context-based responses.

The system uses the following document sources:

- UGC Admission Handbooks
- Faculty Admission Requirements
- Z-score Reports
- Policy Notices

Example questions:

- What subjects are required for Engineering?
- Explain the district quota system.
- What is the Z-score requirement for Medicine?
- Can Bio Science students apply for Agriculture?
- What are the requirements for Computer Science?


System Architecture Diagram


User

  |

  v

Streamlit Web Interface

  |

  v

Router Agent

(Groq Llama 3.1)

  |

  v

Question Classification

  |

  v

ChromaDB Vector Database

  |

  v

Semantic Similarity Search

  |

  v

Retrieved UGC Document Chunks

  |

  v

Retrieval and Synthesis Agent

(Claude Sonnet 4.5)

  |

  v

Generated Answer

  |

  v

Reflection Agent

(Groq Llama 3.1)

  |

  v

Validated Final Response



Technology Stack


Component                     Technology

Programming Language          Python

Frontend                      Streamlit

AI Framework                  LangChain

Router Model                  Llama 3.1 8B Instant (Groq)

Answer Generation Model       Claude Sonnet 4.5 (OpenRouter)

Embedding Model               sentence-transformers/all-MiniLM-L6-v2

Vector Database               ChromaDB

Document Processing           PyPDFLoader

Text Splitting                RecursiveCharacterTextSplitter



Project Structure


ugc-admission-explainer

|

|-- app.py

|-- requirements.txt

|-- README.md

|

|-- data

|   |

|   |-- faculty_sections

|   |

|   |-- zscore_reports

|   |

|   |-- policy_notices

|

|-- chroma_db

|

|-- .streamlit

    |

    |-- secrets.toml



Setup Instructions


1. Clone Repository


git clone https://github.com/Ayesha200352/ugc-admission-explainer.git

cd ugc-admission-explainer



2. Create Virtual Environment


Windows:

python -m venv venv

venv\Scripts\activate


Linux/Mac:

python3 -m venv venv

source venv/bin/activate



3. Install Dependencies


pip install -r requirements.txt



4. Configure API Keys


Create the file:


.streamlit/secrets.toml


Add your API keys:


GROQ_API_KEY="YOUR_GROQ_API_KEY"

OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"


Do not upload this file to GitHub because it contains sensitive information.



5. Add UGC PDF Documents


Add official UGC documents into:


data/

    faculty_sections/

    zscore_reports/

    policy_notices/



6. Run Application


streamlit run app.py


Application runs at:


http://localhost:8501



Model Choice Comparison Table


Model                         Purpose                    Reason Selected


Llama 3.1 8B Instant           Router Agent              Fast response time and low latency for classification tasks


Claude Sonnet 4.5              Answer Generation         Strong reasoning and document understanding


GPT-4o                         Alternative Model         Not selected because of API cost


Gemini 2.5                     Alternative Model         Not selected because Claude provided better document synthesis



Model Selection Strategy


The application uses different models for different responsibilities.


Llama 3.1 8B Instant (Groq):

- Performs question classification
- Routes user queries
- Provides fast response time


Claude Sonnet 4.5:

- Generates final answers
- Uses retrieved document context
- Provides detailed reasoning


Using two models improves system efficiency by combining fast classification with high-quality answer generation.



Agent Communication Diagram


User Question
       |
       v
Router Agent
(Groq Llama 3.1)
       |
       v
Question Category Detection
       |
       v
Retriever
(ChromaDB)
      |
      v
Relevant Document Retrieval
       |
       v
Retrieval and Synthesis Agent
(Claude Sonnet 4.5)
       |
       v
Answer Generation
       |
       v
Reflection Agent
    (Groq)
       |
       v
Final Validated Answer



Agent Responsibilities


Router Agent

The router agent analyses user questions and classifies them into categories:

- Z-score lookup questions
- Eligibility questions
- General admission questions


Retrieval Agent

The retrieval agent searches the ChromaDB vector database and retrieves relevant information from UGC documents.


Synthesis Agent

The synthesis agent receives retrieved information and generates answers using Claude Sonnet 4.5.


Reflection Agent

The reflection agent checks whether the generated answer is supported by retrieved document information.

This reduces unsupported AI responses.



RAG Pipeline Explanation


Step 1: Document Loading


Official UGC PDF documents are loaded using PyPDFLoader.



Step 2: Document Chunking


Documents are divided into smaller sections using:

RecursiveCharacterTextSplitter


Configuration:

Chunk Size = 300

Chunk Overlap = 50


Chunking improves retrieval accuracy by creating smaller searchable sections.



Step 3: Embedding Generation


Each document chunk is converted into vector embeddings using:


sentence-transformers/all-MiniLM-L6-v2



Step 4: Vector Database Storage


The generated embeddings are stored in:


ChromaDB


ChromaDB enables semantic similarity searching between user questions and document content.



Step 5: Retrieval


When a user submits a question:

1. Router Agent identifies the question type.

2. ChromaDB searches for relevant document chunks.

3. The top matching documents are returned.


Retrieval parameter:


k = 6



Step 6: Answer Generation


Claude Sonnet 4.5 receives:

- User question
- Retrieved document context
- Question category


The model generates an answer using only the retrieved information.



Step 7: Reflection Validation


The reflection agent checks whether the answer is supported by the retrieved context.


Possible outputs:


SUPPORTED


or


UNSUPPORTED


This helps reduce hallucinations.



Feature Branch Development


The project follows GitHub feature branch workflow.


Feature branches used:


feature/rag-pipeline

Purpose:

- PDF loading
- Text splitting
- Embedding generation
- ChromaDB retrieval



feature/agent-orchestration

Purpose:

- Multi-agent workflow
- Agent communication
- Pipeline integration



feature/streamlit-ui

Purpose:

- User interface development
- User input handling
- Result display



feature/model-router

Purpose:

- LLM routing logic
- Model selection strategy



Pull Request Workflow


Each feature branch is merged into the main branch through Pull Requests.


Example Pull Request titles:


feat: implement RAG pipeline

feat: add agent orchestration

feat: create Streamlit interface

feat: implement model router



Each Pull Request contains:

- Feature description
- Implementation details
- Testing information



Semantic Commit Messages


The project follows semantic commit conventions.


Examples:


feat: add document retrieval pipeline

feat: integrate Claude synthesis model

feat: create router agent

fix: handle missing PDF documents

fix: improve answer validation

docs: update README documentation

refactor: improve agent structure

test: test RAG responses



Live Streamlit Demo


The application is deployed using Streamlit Cloud.


Live Demo:


https://ugc-admission-explainer-4tgr4pyi4ixqopggyz2ujn.streamlit.app/


Users can use the application to ask questions about:

- University admission eligibility
- Z-score requirements
- District quota system
- Faculty requirements
- UGC admission policies



Known Limitations


- The system depends on the quality of uploaded UGC documents.
- Outdated documents may contain old admission information.
- The application cannot answer questions outside the available document collection.
- Poor-quality scanned PDFs may reduce retrieval accuracy.
- Internet access is required for LLM API communication.
- The system does not replace official UGC admission decisions.



GitHub Project Management


Development progress is managed using:

- Feature branches
- Pull Requests
- Semantic commits
- GitHub Issues or Project Boards



Future Improvements


- Sinhala and Tamil language support
- Conversational memory
- Automatic yearly UGC document updates
- Voice-based interaction
- Better source citation display
- Hybrid keyword and semantic search
- Administrator document upload system


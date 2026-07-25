import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# ============================================
# Page config
# ============================================
st.set_page_config(page_title="UGC Admission & Z-Score Explainer", page_icon="🎓")
st.title("🎓 UGC Admission & Z-Score Eligibility Explainer")
st.caption("Ask about Sri Lankan university admission eligibility, Z-score cutoffs, and district quotas.")

# ============================================
# Load API keys from Streamlit secrets
# ============================================
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["OPENROUTER_API_KEY"] = st.secrets["OPENROUTER_API_KEY"]


# ============================================
# Build the RAG pipeline once, cache it
# ============================================
@st.cache_resource(show_spinner="Setting up the knowledge base (first run only)...")
def build_retriever():
    data_folders = [
        "data/faculty_sections",
        "data/zscore_reports",
        "data/policy_notices",
    ]

    all_docs = []
    for folder in data_folders:
        if not os.path.exists(folder):
            continue
        for filename in os.listdir(folder):
            if filename.endswith(".pdf"):
                path = os.path.join(folder, filename)
                loader = PyPDFLoader(path)
                docs = loader.load()

                # Filter out pages where page_content is None, empty, or non-string
                valid_docs = [
                    doc for doc in docs
                    if doc.page_content and isinstance(doc.page_content, str) and doc.page_content.strip()
                ]
                all_docs.extend(valid_docs)

    if not all_docs:
        st.error("No valid text found in PDF documents! Please ensure PDFs contain readable text and are placed in the data/ folder.")
        st.stop()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    return vectordb.as_retriever(search_kwargs={"k": 6})


@st.cache_resource(show_spinner=False)
def build_models():
    router_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"]
    )

    synthesis_llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4.5",
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=500
    )

    return router_llm, synthesis_llm


retriever = build_retriever()
router_llm, synthesis_llm = build_models()


# ============================================
# Agent 1: Router
# ============================================
def router_agent(question: str, llm) -> dict:
    prompt = f"""Classify this question into exactly one category:
- zscore_lookup: asking about specific Z-score cutoffs or numbers
- eligibility_question: asking about subject/grade requirements for a course
- general_faq: general questions about the admission process

Question: {question}

Respond with ONLY the category name, nothing else."""

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    return {"query": question, "category": category, "from_agent": "router"}


# ============================================
# Agent 2: Retrieval + Synthesis (tool-use pattern)
# ============================================
def retrieval_synthesis_agent(message: dict, retriever, llm) -> dict:
    query = message["query"]
    category = message["category"]

    retrieved_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    sources = [doc.metadata.get("source", "unknown") for doc in retrieved_docs]

    prompt = f"""You are a UGC admission assistant. Answer using ONLY the context below.
If the context doesn't contain the answer, say so honestly.

Category: {category}
Context:
{context}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources,
        "context": context,
        "from_agent": "retrieval_synthesis"
    }


# ============================================
# Reflection step (self-critique pattern)
# ============================================
def reflection_check(answer_message: dict, llm) -> dict:
    prompt = f"""Review this answer against the context.
Does the answer contain ONLY information supported by the context,
or does it include unsupported claims?

Context:
{answer_message['context']}

Answer:
{answer_message['answer']}

Respond with either "SUPPORTED" or "UNSUPPORTED: <brief reason>"."""

    check = llm.invoke(prompt)
    answer_message["reflection_check"] = check.content.strip()
    return answer_message


# ============================================
# Full pipeline orchestration
# ============================================
def full_pipeline(question: str) -> dict:
    router_message = router_agent(question, router_llm)
    result = retrieval_synthesis_agent(router_message, retriever, synthesis_llm)
    result = reflection_check(result, router_llm)
    result["category"] = router_message["category"]
    return result


# ============================================
# Streamlit UI
# ============================================
question = st.text_input("Ask your question:", placeholder="e.g. What subject combination is required for a Bio Science degree?")

if st.button("Get Answer") and question.strip():
    with st.spinner("Thinking..."):
        try:
            result = full_pipeline(question)

            st.subheader("Answer")
            st.write(result["answer"])

            with st.expander("Details (category, sources, reflection check)"):
                st.write(f"**Router category:** {result['category']}")
                st.write(f"**Sources used:**")
                for s in set(result["sources"]):
                    st.write(f"- {s}")
                st.write(f"**Reflection check:** {result['reflection_check']}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("This assistant uses UGC handbook excerpts. Always verify critical decisions against the official UGC handbook.")
from typing import List, Optional
from fastapi import Form, File,APIRouter, Depends,HTTPException
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate


# Your service imports...
from app.services.load_youtube_documents import load_youtube_documents
from app.services.load_wikipedia_documents import load_wikipedia_documents
from app.services.load_pdf_documents import load_pdf_documents
from app.services.build_vector_store import build_vector_store
from app.services.local_llm import call_llm


router = APIRouter()

class RAGResponse(BaseModel):
    answer: str
    sources: List[Source]


@router.post("/rag",response_model=RAGResponse)
async def rag_endpoint(
    question: str = Form(...),
    youtube_url: Optional[str] = Form(None),
    wiki_query: Optional[str] = Form(None),
    pdf: Optional[UploadFile] = File(None),  # Needs UploadFile import
):
    """
    RAG endpoint:
    - Load documents
    - Build vector store
    - Retrieve relevant chunks
    - Call local LLM
    """

    # ---------------------------
    # 1) LOAD + SPLIT DOCUMENTS
    # ---------------------------
    all_docs = []
    yt_docs: List = []
    wiki_docs: List = []
    pdf_docs: List = []

    if youtube_url:
        yt_docs = load_youtube_documents(youtube_url)
        all_docs.extend(yt_docs)

    if wiki_query:
        wiki_docs = load_wikipedia_documents(wiki_query)
        all_docs.extend(wiki_docs)

    if pdf is not None:
        pdf_docs = load_pdf_documents(pdf)
        all_docs.extend(pdf_docs)

    if not all_docs:
        return {
            "error": "Provide at least one source: youtube_url, wiki_query, or pdf."
        }

    # ---------------------------
    # 2) BUILD VECTOR STORE + RETRIEVE
    # ---------------------------
    vector_store = build_vector_store(all_docs)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    retrieved_docs = retriever.invoke(question)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    context_text = format_docs(retrieved_docs)

    # ---------------------------
    # 3) BUILD PROMPT
    # ---------------------------
    prompt = PromptTemplate(
        template=(
            "You are a compliance assistant.\n"
            "Answer ONLY using the context below.\n"
            "If the context is insufficient, say you don't know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
        input_variables=["context", "question"],
    )

    final_prompt = prompt.format(
        context=context_text,
        question=question,
    )

    # ---------------------------
    # 4) CALL LOCAL LLM
    # ---------------------------
    answer = call_llm(
        final_prompt,
        temperature=0.2,
        max_tokens=512,
    )

    # ---------------------------
    # 5) PREPARE SOURCES
    # ---------------------------
    sources = [
        {
            "content": doc.page_content[:400],
            "metadata": doc.metadata,
        }
        for doc in retrieved_docs
    ]

    # ---------------------------
    # 6) RETURN RESPONSE
    # ---------------------------
    return {
        "answer": answer,
        "sources": sources,
    }

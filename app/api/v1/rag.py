from typing import List

from app.services.faiss_loader import load_vector_store
from app.services.llm_client import call_llm
from app.services.reranker import rerank_documents
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    user_id: int
    question: str
    context_ids: List[str]


@router.post("/query")
async def query_rag(request: QueryRequest):

    all_docs = []

    # load FAISS for each context
    for ctx in request.context_ids:
        path = f"vectorstore/{request.user_id}/{ctx}"

        try:
            vs = load_vector_store(path)
        except:
            raise HTTPException(status_code=404, detail=f"Context {ctx} not found")

        retriever = vs.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10},  # small per context
        )

        docs = retriever.invoke(request.question)
        all_docs.extend(docs)

    if not all_docs:
        raise HTTPException(status_code=400, detail="No relevant documents found")

    all_docs = rerank_documents(
        request.question,
        all_docs,
        top_k=5,
    )

    # merge context
    context_text = "\n\n".join(doc.page_content for doc in all_docs)

    # prompt
    prompt = f"""
You are a helpful assistant.
Answer ONLY using the context below.
If not found, say you don't know.

Context:
{context_text}

Question:
{request.question}

Answer:
"""

    answer = call_llm(prompt)

    sources = [
        {"content": doc.page_content[:300], "metadata": doc.metadata}
        for doc in all_docs
    ]

    return {"answer": answer, "sources": sources}

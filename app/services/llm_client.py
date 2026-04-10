import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI



API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=API_KEY
)

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    output: str


def generate(req: GenerateRequest):
    # LangChain invoke
    response = llm.invoke(req.prompt)
    return GenerateResponse(output=response.content)


def call_llm(prompt: str, max_new_tokens: int = 256) -> str:
    print("\n[LLM] Prompt preview:\n", prompt[:400], "...\n")

    output = generate_text(prompt)

    print("[LLM] Output text preview:\n", output[:300], "...\n")
    return output
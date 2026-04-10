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

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    # LangChain invoke
    response = llm.invoke(req.prompt)
    return GenerateResponse(output=response.content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
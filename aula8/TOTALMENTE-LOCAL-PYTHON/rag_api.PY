from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv


app = FastAPI()

# Modelo de entrada
class PromptInput(BaseModel):
    prompt: str

# Configurações do LangChain RAG
embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.3
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# Endpoint para integrar com o bot JS
@app.post("/chat")
async def responder(prompt_input: PromptInput):
    resposta = qa.run(prompt_input.prompt)
    return {"response": resposta}


"""uvicorn rag_api:app --host 0.0.0.0 --port 3000 --reload
"""
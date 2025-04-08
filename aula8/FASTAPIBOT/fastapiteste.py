from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma  # Atualizado
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_huggingface import HuggingFaceEndpoint  # Atualizado
from langchain.chains import RetrievalQA
import os

app = FastAPI()

embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="./chroma_hf_db",
    embedding_function=embedding
)

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",  # <- ESSA LINHA É ESSENCIAL
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.3
)


qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

class Consulta(BaseModel):
    pergunta: str

@app.post("/chat/")
def responder(consulta: Consulta):
    resposta = qa.run(consulta.pergunta)
    return {"resposta": resposta}

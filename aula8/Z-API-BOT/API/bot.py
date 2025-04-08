
from fastapi import FastAPI, Request
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma  # Atualizado
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_huggingface import HuggingFaceEndpoint  # Atualizado
from langchain.chains import RetrievalQA
import os


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

# class Consulta(BaseModel):
#     pergunta: str

# @app.post("/chat/")
# def responder(consulta: Consulta):
#     resposta = qa.run(consulta.pergunta)
#     return {"resposta": resposta}


app = FastAPI()

INSTANCE_ID = "sua_instance"
TOKEN = "seu_token"

@app.post("/whatsapp/")
async def receber_mensagem(request: Request):
    dados = await request.json()
    print("📥 Dados recebidos do Z-API:")
    print(dados)

    pergunta = dados.get("text", {}).get("message")
    #pergunta = dados.get("message")
    if not pergunta:
        return {"ok": True, "msg": "Nada a responder"}

    numero = dados.get("phone")
    print(f"📩 {numero} perguntou: {pergunta}")

    resposta = qa.run(pergunta)
    print(f"🤖 Resposta: {resposta}")

    # Enviar a resposta de volta
    headers = {
        "Content-Type": "application/json",
        "Client-Token":"F069685d93ac046ceaf0109c86552b4f3S"

    }


    res = requests.post(
        url=f"https://api.z-api.io/instances/3DF5537109AC2008AEC732C54B267657/token/ABDB8D2170F899926B0D284D/send-text",
        json={
            "phone": numero,
            "message": resposta,
        },
        headers=headers
    )

        
    if res.status_code != 200:
        print("Erro ao enviar resposta:", res.text)
        return {'erro':True}
    print("📤 Enviando resposta via Z-API")
    print("Status Code:", res.status_code)
    print("Resposta da API:", res.text)
    return {"ok": True}
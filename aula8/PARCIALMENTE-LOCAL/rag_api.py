# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain.chains import RetrievalQA
# from langchain_chroma import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.llms import Ollama
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = FastAPI()

# # Modelo de entrada
# class PromptInput(BaseModel):
#     prompt: str

# # 🔤 Embedding com Ollama/Mistral
# embedding = OllamaEmbeddings(model="mistral")

# # 🧠 Vetorstore com Chroma
# vectorstore = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embedding
# )

# # 🤖 LLM local também com Ollama/Mistral
# llm = Ollama(model="mistral")

# # 🔗 RAG
# qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=vectorstore.as_retriever()
# )

# # Endpoint da API
# @app.post("/chat")
# async def responder(prompt_input: PromptInput):
#     resposta = qa.run(f"Responda em português: {prompt_input.prompt}")

#     return {"response": resposta}
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

# 0. Carrega variáveis de ambiente se necessário
load_dotenv()

# 1. Inicializar o FastAPI
app = FastAPI()

# 2. Modelo de entrada (input do JS)
class PromptInput(BaseModel):
    prompt: str

# 3. Embedding com Ollama (usa o mistral)
embedding = OllamaEmbeddings(model="mistral")

# 4. Recuperar documentos vetorizados salvos no Chroma
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

# 5. LLM local com Ollama/Mistral
llm = Ollama(model="mistral")

# 6. Memória conversacional
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 7. Prompt personalizado (ajustável)
system_prompt = """
Você é um atendente virtual da empresa TechSolutions. 
Seu papel é responder de forma clara, educada e objetiva, 
como se fosse um funcionário treinado no setor de suporte ao cliente.

- Você é um assistente inteligente que sempre responde em português.
- Use uma linguagem formal e acolhedora.
- Se a resposta não for encontrada na base de conhecimento, oriente o usuário a entrar em contato pelo e-mail suporte@techsolutions.com.
- Nunca invente informações. Seja honesto e direto.
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}\n\nContexto:\n{context}")
])

# 8. Cadeia RAG com conversação
chatbot = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt_template}
)

# 9. Endpoint FastAPI para receber o prompt
@app.post("/chat")
async def responder(prompt_input: PromptInput):
    resultado = chatbot.invoke({"question": prompt_input.prompt})
    resposta_final = resultado["answer"].strip()
    return {"response": resposta_final}

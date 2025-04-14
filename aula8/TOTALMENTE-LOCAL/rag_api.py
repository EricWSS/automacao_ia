import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaEmbeddings, OllamaLLM
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
    persist_directory="chroma_db",
    embedding_function=embedding
)

# 5. LLM local com Ollama/Mistral
llm = OllamaLLM(model="mistral")

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

- Construa frases curtas e objetivas. Os textos só podem ter no MÁXIMO 100 caracteres.
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
    try:
        print("🧠 Pergunta recebida:", prompt_input.prompt)

        retriever = vectorstore.as_retriever()
        print("🔍 Retriever carregado")

        # resultado = chatbot.invoke({"question": prompt_input.prompt})
        resultado = chatbot.invoke({"question": prompt_input.prompt})


        print('TYPE = ',type(resultado))
        print("📤 Resultado do invoke:", resultado)

        resposta_final = resultado["answer"].strip()
        print("✅ Resposta final:", resposta_final)

        return {"response": resposta_final}

    except Exception as e:
        import traceback
        print("❌ Erro interno:")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


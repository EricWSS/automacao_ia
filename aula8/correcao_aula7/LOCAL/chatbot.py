from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA

# 1. Carrega o banco vetorial persistido
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OllamaEmbeddings(model="mistral")
)

# 2. Inicializa a LLM local (via Ollama)
llm = ChatOllama(model="mistral")

# 3. Cria a cadeia de RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 4. Permite fazer perguntas quantas vezes quiser
while True:
    pergunta = input("Faça uma pergunta (ou digite 'sair'): ")
    if pergunta.lower() == "sair":
        break
    resposta = qa.run(pergunta)
    print("Bot:", resposta)

import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatHuggingFace

# 1. Recarregar os embeddings da Hugging Face
embedding_function = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2. Recarregar a base vetorial já criada
vectorstore = Chroma(
    persist_directory="./chroma_hf_db",
    embedding_function=embedding_function
)

# 3. LLM pela API da Hugging Face
llm = ChatHuggingFace(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  # ou outro modelo de chat
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# 4. Montar o RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 5. Fazer perguntas em loop
while True:
    pergunta = input("Pergunte algo (ou 'sair'): ")
    if pergunta.lower() == "sair":
        break
    resposta = qa.run(pergunta)
    print("Bot:", resposta)

from langchain.chains import RetrievalQA
from criando_vetores_no_banco_API1 import vectorstore
from langchain_community.llms import HuggingFaceHub
import os

pergunta = "Como posso solicitar um reembolso?"

resultados = vectorstore.similarity_search(pergunta, k=2)

# LLM da Hugging Face (API)
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    model_kwargs={"temperature": 0.7, "max_length": 512},
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# Cria a cadeia de perguntas e respostas
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 5. Fazer uma pergunta de teste
resposta = qa.run(pergunta)
print("Bot:", resposta)

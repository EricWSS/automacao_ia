from langchain.chains import RetrievalQA
from aula7.LOCAL.criando_vetores_no_banco_local1 import vectorstore
from langchain_community.llms import Ollama

pergunta = "Como posso solicitar um reembolso?"

resultados = vectorstore.similarity_search(pergunta, k=2)

# Inicializa o modelo local Mistral via Ollama
llm = Ollama(model="mistral", temperature=0)

# Cria a cadeia de perguntas e respostas
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 5. Fazer uma pergunta de teste
resposta = qa.run(pergunta)
print("Bot:", resposta)

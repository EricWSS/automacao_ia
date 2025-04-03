from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# 1. Carregar o PDF
loader = PyPDFLoader("politica_reembolso_infinitytech.pdf")
documentos = loader.load()

# 2. Quebrar o texto em blocos menores (chunking)
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
blocos = splitter.split_documents(documentos)

# 3. Gerar embeddings e salvar no ChromaDB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documentos=blocos,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. Criar um RAG (recupera e gera resposta)
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="SUA_CHAVE_OPENAI"),
    retriever=vectorstore.as_retriever()
)

# 5. Fazer uma pergunta de teste
pergunta = "Como posso solicitar um reembolso?"
resposta = qa.run(pergunta)
print("Bot:", resposta)

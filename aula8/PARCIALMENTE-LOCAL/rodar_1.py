""" RODAR ESSE ARQUIVO PRIMEIRO """
""" Esse arquivo é o responsável por SALVAR no banco de dados ChromaDB 
    os vetores uma única vez a partir do documento 'PDF' que está na pasta."""

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

# Carregando PDF
loader = PyPDFLoader(r"D:\automacao_ia\aula8\correcao_aula7\LOCAL\politica_reembolso_infinitytech.pdf")
documentos = loader.load()

# Chunking
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
blocos = splitter.split_documents(documentos)

# Vetorizando com modelo local (Ollama)
embedding = OllamaEmbeddings(model="mistral")

# Criando e salvando ChromaDB
vectorstore = Chroma.from_documents(
    documents=blocos,
    embedding=embedding,
    persist_directory="./chroma_db"
)


print("Base vetorizada criada com sucesso!")

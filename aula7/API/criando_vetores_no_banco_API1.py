from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os


# 1. Carregar o PDF
loader = PyPDFLoader("D:/automacao_ia/aula7/politica_reembolso_infinitytech.pdf")
documentos = loader.load()

# 2. Quebrar o texto em blocos menores (chunking)
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
blocos = splitter.split_documents(documentos)

# 3. Embeddings via HF Inference API
embedding_function = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Gerar embeddings e salvar no ChromaDB
vectorstore = Chroma.from_documents(
    documents=blocos,
    embedding=embedding_function,
    persist_directory="./teste_db_API"
)
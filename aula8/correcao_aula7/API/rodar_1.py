import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import Chroma

# 1. Carregar o PDF
loader = PyPDFLoader(r"D:\automacao_ia\aula8\correcao_aula7\API\politica_reembolso_infinitytech.pdf")
documentos = loader.load()

# 2. Dividir em chunks
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
blocos = splitter.split_documents(documentos)

# 3. Configurar os embeddings via Hugging Face
embedding_function = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Criar e salvar o banco vetorial
vectorstore = Chroma.from_documents(
    documents=blocos,
    embedding=embedding_function,
    persist_directory="./chroma_hf_db"
)

print("✅ Vetorização concluída e persistida.")

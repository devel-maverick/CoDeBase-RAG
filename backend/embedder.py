from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import EMBEDDING_MODEL,CHROMA_DB_PATH

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

def get_vector_db(documents,collection_name):
    print(f"embeddings {len(documents)}")
    embeddings=get_embeddings()
    vectorstore=Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_PATH
    )
    print(f"Vector store created {vectorstore}")
    return vectorstore
    
def load_vectorstore(collection_name):
    embeddings=get_embeddings()
    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_name=collection_name
    )

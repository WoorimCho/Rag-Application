# import os
# from langchain_ollama import OllamaEmbeddings
# from langchain_chroma import Chroma

from langchain_ollama import OllamaEmbeddings
import os
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

CHROMA_PATH = os.getenv('CHROMA_PATH', 'chroma')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'local-rag')
TEXT_EMBEDDING_MODEL = os.getenv('TEXT_EMBEDDING_MODEL', 'nomic-embed-text')

def get_vector_db():
    embedding = OllamaEmbeddings(
        model=TEXT_EMBEDDING_MODEL,
        base_url=os.getenv('OLLAMA_API_URL', 'http://192.168.1.41:60001')
        #api_key=os.getenv('OLLAMA_API_KEY', None)
    )
    
    index = faiss.IndexFlatL2(len(embedding.embed_query("hello world")))

    db = FAISS(
        embedding_function=embedding,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    # db = Chroma(
    #     collection_name=COLLECTION_NAME,
    #     persist_directory=CHROMA_PATH,
    #     embedding_function=embedding
    # )

    return db
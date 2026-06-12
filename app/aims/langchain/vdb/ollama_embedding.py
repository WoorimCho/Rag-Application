import os

from app.aims.agent.agent_types import VDBType
from app.aims.langchain.vdb.embedding_base import EmbeddingBase

import faiss
# import chroma
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain_chroma import Chroma

from langchain_ollama import OllamaEmbeddings

from dotenv import load_dotenv
load_dotenv()

class OllamaEmbedding(EmbeddingBase):

    def get_database(self):
        match self.vdb_type:
            case VDBType.CHROMA:
                return self.__get_chroma_db()
            case VDBType.FAISS:
                return self.__get_faiss_db()
            case _:
                raise ValueError(f"Unsupported vdb_type: {self.vdb_type}")

        return None
    

    def __get_chroma_db(self): 
        embedding = OllamaEmbeddings(
            model= self.embedding_model,
            base_url=os.getenv('OLLAMA_API_URL', None),
            # api_key=os.getenv('OLLAMA_API_KEY', None)
        )
        return Chroma(
            collection_name=os.getenv('COLLECTION_NAME', None),
            persist_directory=os.getenv('CHROMA_PATH', None),
            embedding_function=embedding
        )
          

    def __get_faiss_db(self):
        TEXT_EMBEDDING_MODEL = os.getenv('TEXT_EMBEDDING_MODEL', 'nomic-embed-text')
        embedding = OllamaEmbeddings(
            model=TEXT_EMBEDDING_MODEL,
            base_url=os.getenv('OLLAMA_API_URL', 'http://192.168.1.41:60001')
        )

        index = faiss.IndexFlatL2(len(embedding.embed_query("hello world")))

        return FAISS(
            embedding_function=embedding,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
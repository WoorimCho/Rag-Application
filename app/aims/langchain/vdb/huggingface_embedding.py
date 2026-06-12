import os

import faiss
from app.aims.agent.agent_types import VDBType
from app.aims.langchain.vdb.embedding_base import EmbeddingBase
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma, FAISS
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS


class HuggingFaceEmbedding(EmbeddingBase):

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
        print(f" HF - VDB CHROMA embedding mode = [{self.embedding_model}]")
        embedding = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )
        return Chroma(
            collection_name=os.getenv('COLLECTION_NAME', ''),
            persist_directory=os.getenv('CHROMA_PATH', None),
            embedding_function=embedding
        )

    
    def __get_faiss_db(self):
        print(f" HF - VDB FAISS embedding mode = [{self.embedding_model}]")
        embedding = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )

        from langchain.docstore.in_memory import InMemoryDocstore

        index = faiss.IndexFlatL2(len(embedding.embed_query("hello world")))

        return FAISS(
            embedding_function=embedding,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )


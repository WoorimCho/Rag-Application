import os
#from langchain_huggingface import HuggingFaceEmbeddings
from app.aims import AGENT_CONFIG
from app.aims.agent.agent_types import LLMProvider
from app.aims.langchain.vdb.huggingface_embedding import HuggingFaceEmbedding
from app.aims.langchain.vdb.ollama_embedding import OllamaEmbedding

from dotenv import load_dotenv
load_dotenv()

class VdbAdapter:

    def __init__(self, agent_config: AGENT_CONFIG):
        self.config = agent_config

    def get_vector_db(self):
        match self.config.llm_provider:
            case LLMProvider.OLLAMA:        return self.__get_ollama_db()
            case LLMProvider.HUGGING_FACE:  return self.__get_huggingface_db()
            case _:
                raise ValueError(f"Unsupported llm_provider: {self.config.llm_provider}")



    def __get_ollama_db(self):
        embedding = OllamaEmbedding(
            embedding_model=self.config.ollama.embedding_model,
            vdb_type=self.config.ollama.vdb_type
        )
        return embedding.get_database()
    
    def __get_huggingface_db(self):        
        embedding = HuggingFaceEmbedding(
            embedding_model=self.config.huggingface.embedding_model,
            vdb_type=self.config.huggingface.vdb_type
        ) 
        return embedding.get_database()
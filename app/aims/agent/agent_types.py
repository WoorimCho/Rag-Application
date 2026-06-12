from enum import Enum


class AgentActionType(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    READ = 4

class LLMProvider(Enum):
    OPENAI = "openai"    
    OLLAMA = "ollama"
    HUGGING_FACE = "hugging_face"

class VDBType(Enum):
    CHROMA = "chroma"
    FAISS = "faiss"


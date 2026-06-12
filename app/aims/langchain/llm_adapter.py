from app.aims import AGENT_CONFIG
from app.aims.agent.agent_types import LLMProvider
from app.aims.langchain.llm.huggingface_llm import HuggingFaceLLM
from app.aims.langchain.llm.llm_base import LLMBase
from app.aims.langchain.llm.ollama_llm import OllamaLLM


class LlmAdapter:
    #llm: LLMBase

    def __init__(self, agent_config: AGENT_CONFIG):
        self.config = agent_config

    # def start(self, vdb):
    #     self.llm = self.get_llm(vdb)

    # def query(self, message: str):
    #     if self.llm is None:
    #         raise ValueError("LLM has not been initialized. Call start() first.")
    #     return self.llm.query(message)

    def get_llm(self, vdb) -> LLMBase:
        llm: LLMBase = None
        if self.config.llm_provider == LLMProvider.OLLAMA:
            llm = OllamaLLM(self.config)
        elif self.config.llm_provider == LLMProvider.HUGGING_FACE:
            llm = HuggingFaceLLM(self.config)
        else:
            raise ValueError(f"Unsupported llm_provider: {self.config.llm_provider}")
        return llm.build(vdb)
    
 


    


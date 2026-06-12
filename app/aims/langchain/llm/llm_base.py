from typing import Any

from app.aims import AGENT_CONFIG

class LLMBase:
    def __init__(self, agent_config: AGENT_CONFIG):
        self.config = agent_config

    def build(self, vdb: Any) -> Any:
        # Logic to build and return the LLM instance
        pass

    def query(self, message: str) -> Any:
        # Logic to query the LLM instance
        pass
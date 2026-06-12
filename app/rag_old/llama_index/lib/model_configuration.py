from app.rag.llama_index import llm_models


class ModelConfiguration:

    @staticmethod
    def get_model_info(name):
        for m in llm_models:
            if name == m.name:
                return m
        return None
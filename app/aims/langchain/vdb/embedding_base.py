from typing import Any


class EmbeddingBase:

    def __init__(self, embedding_model, vdb_type):
        self.embedding_model = embedding_model
        self.vdb_type = vdb_type

    def get_database(self) -> Any:
        return None

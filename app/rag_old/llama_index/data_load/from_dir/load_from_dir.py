import os

#os.environ["REPLICATE_API_TOKEN"] = "YOUR_REPLICATE_API_TOKEN"

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.replicate import Replicate
from transformers import AutoTokenizer

from app.rag.llama_index.lib.model_configuration import ModelConfiguration


class LoadDataFromDirectory:
    index = None

    def __init__(self):
        mcfg = ModelConfiguration.get_model_info("llama-3.2-3b")    # llama2_7b_chat, llama-3.2-3b, deepseek-r1-7b

        # Set the LLM
        Settings.llm = Replicate(
            model=mcfg.model,
            temperature=mcfg.temperature,
            additional_kwargs={
                "top_p": mcfg.additional_kwargs.top_p,
                "max_new_tokens": mcfg.additional_kwargs.max_new_tokens},
        )

        # set tokenizer to match LLM
        Settings.tokenizer = AutoTokenizer.from_pretrained(
            "NousResearch/Llama-2-7b-chat-hf"
        )

        # set the embed model
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def run(self, data_path):
        documents = SimpleDirectoryReader("YOUR_DATA_DIRECTORY").load_data()
        self.index = VectorStoreIndex.from_documents(
            documents,
        )
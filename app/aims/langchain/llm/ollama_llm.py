from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

from app.aims.langchain.llm.prompt_builder import PromptBuilder
from app.aims.langchain.llm.llm_base import LLMBase


class OllamaLLM(LLMBase):
    chain = None

    def build(self, vdb):
        llm = ChatOllama(model=self.config.ollama.llm_model, 
                    base_url=self.config.ollama.api_url, 
                    temperature=0.1)

        builder = PromptBuilder(prompt_type="default")
        query_prompt, prompt = builder.build()

        base_retriever = vdb.as_retriever(search_kwargs={'k': 10})
        retriever = MultiQueryRetriever.from_llm(
            base_retriever,
            llm,
            prompt=query_prompt
        )
        self.chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )

        
    def query(self, message: str):
        return self.chain.invoke({"input": message})
#from langchain_huggingface import ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
#from langchain.llms import HuggingFaceHub
#from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint

#from langchain_community.vectorstores import Chroma



from app.aims.langchain.llm.llm_base import LLMBase
from app.aims.langchain.llm.prompt_builder import PromptBuilder


class HuggingFaceLLM(LLMBase):
    # retriever = None
    # query_prompt = None

    # def build(self, vdb=None):
    #     builder = PromptBuilder(prompt_type="default")
    #     self.query_prompt, prompt = builder.build()
    
    #     llm = HuggingFaceEndpoint(
    #         repo_id="microsoft/Phi-3-mini-4k-instruct",
    #         task="text-generation",
    #         max_new_tokens=512,
    #         do_sample=False,
    #         repetition_penalty=1.03,
    #     )
    #     self.retriever = ChatHuggingFace(llm=llm, verbose=True)  



    chain = None

    def build(self, vdb):
        # Initialize Hugging Face LLM
        llm = HuggingFaceEndpoint(
            #model=self.config.huggingface.llm_model,
            repo_id=self.config.huggingface.llm_model,
            huggingfacehub_api_token=self.config.huggingface.api_token,
            #model_kwargs={"temperature": 0.1}
            temperature=0.1
        )

        # Build prompt
        builder = PromptBuilder(prompt_type="default")
        query_prompt, prompt = builder.build()

        # Set up retriever
        base_retriever = vdb.as_retriever(search_kwargs={'k': 10})
        retriever = MultiQueryRetriever.from_llm(
            base_retriever,
            llm,
            prompt=query_prompt
        )

        # Build chain
        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def query(self, message: str):
        if self.chain is None:
            raise RuntimeError("The LLM chain has not been built. Call build() before querying.")
        return self.chain.invoke({"input": message})


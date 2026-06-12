import os
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
# from app.aims.api.vector.get_vector_db import get_vector_db
from app.aims.langchain.vdb_adapter import VdbAdapter
from app.aims import AGENT_CONFIG
from app.aims.agent.agent_types import LLMProvider
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint


LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://192.168.1.41:60001')

class Query_Handler():

    query = None
    QUERY_PROMPT = None
    prompt = None
    llm = None
    retriever = None
    db = None

    def vdb_select(self):
        llm_provider = AGENT_CONFIG.llm_provider            # os.getenv("LLM_PROVIDER")
        embedding_model = AGENT_CONFIG.embedding_model      # os.getenv("TEXT_EMBEDDING_MODEL")
        vdb_type = AGENT_CONFIG.vdb_type
        return VdbAdapter(llm_provider,embedding_model,vdb_type).get_vector_db()
    
    def get_prompt(self):
        global QUERY_PROMPT, prompt
        
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI assistant. Generate five reworded versions of the user question
            to improve document retrieval. Original question: {question}""",
        )

        template = "Answer the question based ONLY on this context:" \
        "{context}" \
        "Question: {question}"

        prompt = ChatPromptTemplate.from_template(template)
    
    def __init__(self, input):
        global query
        query = input
    
    def search(self):
        global llm, retriever
        match AGENT_CONFIG.llm_provider:
            case  LLMProvider.HUGGING_FACE:
                llm = HuggingFaceEndpoint(
                    repo_id="microsoft/Phi-3-mini-4k-instruct",
                    task="text-generation",
                    max_new_tokens=512,
                    do_sample=False,
                    repetition_penalty=1.03,
                )
                retriever = ChatHuggingFace(llm=llm, verbose=True)  
                return retriever(...).invoke(QUERY_PROMPT)
                # return db.aembed_query(QUERY_PROMPT)

            case  LLMProvider.OLLAMA:
                llm = ChatOllama(model=LLM_MODEL, 
                         base_url=OLLAMA_API_URL, 
                         temperature=0.1)
                
                base_retriever = db.as_retriever(search_kwargs={'k': 10})
                retriever = MultiQueryRetriever.from_llm(
                    base_retriever,
                    llm,
                    prompt=QUERY_PROMPT
                )
                chain = (
                        {"context": retriever, "question": RunnablePassthrough()}
                        | prompt
                        | llm
                        | StrOutputParser()
                )
                return chain.invoke(input)
                
        
    def run(self):
        global db
        if query:
            db = self.vdb_select()
            self.get_prompt()
            return self.search()
        else:
            return None
    




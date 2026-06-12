# import os
# from langchain_ollama import ChatOllama
# from langchain.prompts import ChatPromptTemplate, PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain.retrievers.multi_query import MultiQueryRetriever
# from .get_vector_db import get_vector_db

from app.aims.api.query.query_handler import Query_Handler

# LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
# OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://192.168.1.41:60001')


# # Function to get the prompt templates for generating alternative questions and answering based on context
# def get_prompt():
#     QUERY_PROMPT = PromptTemplate(
#         input_variables=["question"],
#         template="""You are an AI assistant. Generate five reworded versions of the user question
#         to improve document retrieval. Original question: {question}""",
#     )

#     template = "Answer the question based ONLY on this context:" \
#     "{context}" \
#     "Question: {question}"

#     prompt = ChatPromptTemplate.from_template(template)

#     return QUERY_PROMPT, prompt


# Main function to handle the query process
def query(input):
    query_handler = Query_Handler(input)
    return query_handler.run()
    
    # if input:
    #     # Initialize the language model with the specified model name
    #     llm = ChatOllama(model=LLM_MODEL, 
    #                      base_url=OLLAMA_API_URL, 
    #                      temperature=0.1)
    #     # Get the vector database instance
    #     db = get_vector_db()
    #     # Get the prompt templates
    #     QUERY_PROMPT, prompt = get_prompt()

    #     # Set up the retriever to generate multiple queries using the language model and the query prompt
    #     # Increase k to fetch more documents, hopefully including older ones.
    #     base_retriever = db.as_retriever(search_kwargs={'k': 10})
    #     retriever = MultiQueryRetriever.from_llm(
    #         base_retriever,
    #         llm,
    #         prompt=QUERY_PROMPT
    #     )

    #     # Define the processing chain to retrieve context, generate the answer, and parse the output
    #     chain = (
    #             {"context": retriever, "question": RunnablePassthrough()}
    #             | prompt
    #             | llm
    #             | StrOutputParser()
    #     )

    #     response = chain.invoke(input)

    #     return response

    # return None

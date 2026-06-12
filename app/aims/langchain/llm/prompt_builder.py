from langchain.prompts import ChatPromptTemplate, PromptTemplate


class PromptBuilder:
    def __init__(self, prompt_type: str):
        self.prompt_type = prompt_type


    def build(self):
        query_prompt = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI assistant. Generate five reworded versions of the user question
            to improve document retrieval. Original question: {question}""",
        )

        template = "Answer the question based ONLY on this context:" \
        "{context}" \
        "Question: {question}"

        prompt = ChatPromptTemplate.from_template(template)
        return query_prompt, prompt
from typing import Optional
import openai
from pydantic import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class RelevantItem(BaseModel):
    name: str = Field(
        description="The name of the section, article, ordanance, or piece of legislation."
    )
    relevance: str = Field(
        description="A short summary of how the item is relevant to the question."
    )


class ApplicationResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    relevant_documents: list[RelevantItem] = Field(
        description="A list of relevant items (section, article, ordanance, or piece of legislation)"
    )


def answer_question_with_docs(model, db, query: str):
    documents = db.similarity_search(query)

    print("answering question with docs")
    for d in documents:
        print(d.metadata)
        print(d.page_content)
        print()

    template_str = """
    These are excerpts from the SF planning code. Use them when answering the user's question:
    {documents}
    {format_instructions}

    This is the user's question:
    {query}
    """

    parser = PydanticOutputParser(pydantic_object=ApplicationResponse)
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["documents", "query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_model = prompt | model
    output = prompt_and_model.invoke(
        {
            "documents": "\n\n".join(d.page_content for d in documents),
            "query": query,
        }
    )
    response = parser.invoke(output)
    return response


def ask_question(model, db, raw_application: Optional[str], query: str):
    documents = db.similarity_search(raw_application + " " + query)

    full_prompt = f""",
        {raw_application}\n\n
        {(chr(10) + chr(10)).join([d.page_content for d in documents])},
    """

    template_str = "Given an SF Planning application for a new development answer the following question: \n{query}\n"

    prompt = PromptTemplate(template=template_str, input_variables=["query"])

    prompt_and_model = prompt | model
    response = prompt_and_model.invoke({"query": full_prompt})

    return response

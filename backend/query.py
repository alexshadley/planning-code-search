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
    summary: str = Field(description="A summary of the application")
    relevant_documents: list[RelevantItem] = Field(
        description="A list of relevant items (section, article, ordanance, or piece of legislation)"
    )


def find_relavant_docs(model, db, raw_application: str):
    documents = db.similarity_search(raw_application)

    full_prompt = f""",
        {raw_application}\n\n
        {(chr(10) + chr(10)).join([d.page_content for d in documents])},
    """

    template_str = "Given an SF Planning application for a new development, give a summary of relavant sections, articles, ordanances, or pieces of legislation. \n{format_instructions}\n{query}\n"

    parser = PydanticOutputParser(pydantic_object=ApplicationResponse)
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_model = prompt | model
    output = prompt_and_model.invoke({"query": full_prompt})
    response = parser.invoke(output)

    return response


def ask_question(model, db, raw_application: str, query: str):
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

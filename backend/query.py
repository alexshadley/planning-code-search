
import openai
from pydantic import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class RelevantItem(BaseModel):
    name: str = Field(description="The name of the section, article, ordanance, or piece of legislation.")
    relevance: str = Field(description="A short summary of how the item is relevant to the question.")

class ApplicationResponse(BaseModel):
    summary: str = Field(description="A summary of the application")
    relevant_documents: list[RelevantItem] = Field(description="A list of relevant items (section, article, ordanance, or piece of legislation)")


def query_documents(model, db, query):

    documents = db.similarity_search(query)

    full_prompt = f''',
        {query},
        {(chr(10) + chr(10)).join([d.page_content for d in documents])},
    '''

    parser = PydanticOutputParser(pydantic_object=ApplicationResponse)
    prompt = PromptTemplate(
        template= "You provide summaries of relavant documents to a particular question concerning SF Housing regulations. \n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_model = prompt | model
    output = prompt_and_model.invoke({"query": full_prompt})
    response = parser.invoke(output)



    return response



from typing import List, Optional
import openai
from pydantic import BaseModel, Field
import csv
import os
from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class RelevantItem(BaseModel):
    name: str = Field(
        description="The name of the section, article, ordanance, or piece of legislation."
    )
    relevance: str = Field(
        description="A short summary of how the item is relevant to the question."
    )
    rid: str = Field(description="The rid associated with this excerpt")


class ApplicationResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    relevant_documents: list[RelevantItem] = Field(
        description="A list of relevant items (section, article, ordanance, or piece of legislation)"
    )


def answer_question_with_docs(
        model, embeddings_model, pinecone_index, query_parts: List[str]
):
    matches = []
    for part in query_parts:
        query_embeddings = embeddings_model.embed_query(part)
        matches.extend(
            pinecone_index.query(
                vector=query_embeddings, top_k=3, include_metadata=True
            )["matches"]
        )

    template_str = """
    These are excerpts from the SF planning code. Use them when answering the user's question:
    {documents}
    {format_instructions}

    This is the user's question:
    {query}
    """
    print(template_str)

    parser = PydanticOutputParser(pydantic_object=ApplicationResponse)
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["documents", "query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    documents_text = "\n\n".join(str(d["metadata"]) for d in matches)
    print("docs", documents_text)

    prompt_and_model = prompt | model
    output = prompt_and_model.invoke(
        {
            "documents": documents_text,
            "query": "\n".join(query_parts),
        }
    )
    response = parser.invoke(output)
    print(response.answer)
    try:
        save_to_db(query_parts, documents_text, response.answer)
    except Exception:  #TODO: Use logger to log exception
        print('Failed to save to db')
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


def save_to_db(query, documents, response):
    """Use a local csv file to save queries, contexts, and responses. Creates csv if needed."""
    # Convert lists to string
    def format_value(value):
        if isinstance(value, list):
            return ','.join(str(v) for v in value)
        return str(value)
    
    print('saving to db')
    # Check if db.csv exists
    file_exists = os.path.isfile('./db.csv')

    # append or write
    with open('./db.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # write columns if needed
        if not file_exists:
            writer.writerow(['timestamp', 'query', 'context', 'response'])

        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            format_value(query),
            format_value(documents),
            format_value(response)
        ])

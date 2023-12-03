from langchain.embeddings import OpenAIEmbeddings

import os

from backend.load import init_db_from_documents

import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    documents = ["san_francisco-ca-2.html"]
    init_db_from_documents(documents, embeddings_model)

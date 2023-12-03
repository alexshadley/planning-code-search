from langchain.embeddings import OpenAIEmbeddings

import os

from backend.load import init_db_from_documents

if __name__ == '__main__':
        
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    embeddings_fn = embeddings_model.embed

    documents = ["san_francisco-ca-1.txt"]
    init_db_from_documents(documents, embeddings_model)
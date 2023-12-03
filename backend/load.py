
from typing import List
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma



def chunk_document(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        length_function = len,
        add_start_index = True,
    )

    chunks = splitter.create_documents([text])
    return chunks

def init_db_from_documents(document_filenames: List[str], embeddings_model: OpenAIEmbeddings):
    chunks = []
    for doc in document_filenames:
        chunks.extend(chunk_document(doc))

    db = Chroma.from_documents(chunks, embeddings_model, persist_directory='./chroma_db')

    return db


def load_document(filedir: str):
    with open(filedir, encoding='latin-1') as f:
        planning_code = f.read()

    chunks = chunk_document(planning_code)

    return chunks

    
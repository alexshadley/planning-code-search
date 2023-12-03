import json
from typing import Optional
from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
import tempfile

import os
import dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI

from backend.load import init_db_from_documents
from backend.query import ask_question, find_relavant_docs

from pydantic import BaseModel

dotenv.load_dotenv(dotenv.find_dotenv())


class QueryBody(BaseModel):
    query: Optional[str]
    application: str


app = FastAPI()

db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

model = ChatOpenAI(model='gpt-4-1106-preview')


FRONTEND_PORT = os.getenv("PORT", str(3000))

origins = [
    "http://localhost:" + FRONTEND_PORT,
    "https://localhost:" + FRONTEND_PORT,
    # actual url if we host this somewhere
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse_pdf")
async def parse_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    text = "".join(p.extract_text() for p in reader.pages)
    return {"text": text}


@app.post("/query")
async def query(query_body: QueryBody):
    summary = find_relavant_docs(model, db, query_body.application)
    answer = ''
    if query_body.query is not None:
        answer = ask_question(model, db, query_body.application, query_body.query).content
    return {"summary": summary, "answer": answer}

from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
import tempfile

import os
import dotenv

import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI

from backend.load import init_db_from_documents
from backend.query import query_documents

from pydantic import BaseModel

dotenv.load_dotenv(dotenv.find_dotenv())


class QueryBody(BaseModel):
    query: str
    application: str


app = FastAPI()

embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

documents = ["../san_francisco-ca-1.txt"]

db = init_db_from_documents(documents, embeddings_model)

client = OpenAI()


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
    print(query_body)
    return {"response": "idk figure it out"}


# app.mount("/app", StaticFiles(directory="build"), name="root")


@app.get("/process_application")
async def process_application():
    return RedirectResponse(url="app/index.html")


@app.get("/answer_question")
async def answer_question():
    return RedirectResponse(url="app/index.html")

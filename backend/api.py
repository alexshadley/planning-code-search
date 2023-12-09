import json
from typing import Optional
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader

import os
import dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI

from backend.query import answer_question_with_docs

from pydantic import BaseModel

from pathlib import Path


dotenv.load_dotenv(dotenv.find_dotenv())


class QueryBody(BaseModel):
    query: str


app = FastAPI()

db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

model = ChatOpenAI(model="gpt-4-1106-preview")


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

frontend_path = Path(__file__).parent.parent / "frontend" / "build"

app.mount("/static", StaticFiles(directory=frontend_path / "static"), name="static")


@app.get("/")
async def read_root():
    # return "hi"
    return FileResponse(frontend_path / "index.html")


@app.post("/api/parse_pdf")
async def parse_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    text = "".join(p.extract_text() for p in reader.pages)
    return {"text": text}


@app.post("/api/query")
async def query(query_body: QueryBody):
    answer = answer_question_with_docs(model, db, query_body.query)
    return {
        "answer": answer,
    }

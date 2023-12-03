
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import dotenv

import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI

from backend.load import init_db_from_documents
from backend.query import query_documents

dotenv.load_dotenv(dotenv.find_dotenv())

app = FastAPI()

embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

documents = [
    '../san_francisco-ca-1.txt'
]

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
    allow_headers=["*"]
)

# app.mount("/app", StaticFiles(directory="build"), name="root")

@app.get("/process_application")
async def process_application():
    return RedirectResponse(url="app/index.html")

@app.get("/answer_question")
async def answer_question():
    return RedirectResponse(url="app/index.html")
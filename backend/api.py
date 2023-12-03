
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

app = FastAPI()

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

@app.get("/")
async def index():
    return RedirectResponse(url="app/index.html") # replace with path to index.html

# app.mount("/app", StaticFiles(directory="build"), name="root")

@app.get("/process_application")
async def process_application():
    return RedirectResponse(url="app/index.html")

@app.get("/answer_question")
async def answer_question():
    return RedirectResponse(url="app/index.html")
import os
from fastapi import FastAPI
from embeddings.embeddings import get_closest_match

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ask")
async def ask_question(query: str):
    return {get_closest_match(query)}

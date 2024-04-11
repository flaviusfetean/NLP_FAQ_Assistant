from fastapi import FastAPI
from base.retrieve import get_closest_match
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ask")
async def ask_question(query: dict):
    return {get_closest_match(query['query'])}

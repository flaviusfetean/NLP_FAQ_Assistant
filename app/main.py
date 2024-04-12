from fastapi import FastAPI
from base.retrieve import get_closest_match, assistant
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


@app.post("/ask-question")
async def ask_question(query: dict):
    return get_closest_match(query['user_question'])


@app.post("/set_api_key")
async def send_api_key(key: dict):
    success = assistant.register_key(key['apiKey'])

    return {"Server: " + ("Successfully connected to openai server" if success else
                          "Invalid API key. You will continue receiving responses from the local model.")}

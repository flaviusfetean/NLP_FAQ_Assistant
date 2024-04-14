import openai
from config import api_key
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "172.16.200.13")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "orca-mini")


class Assistant:
    def __init__(self):
        self.client_type, self.client = self.init_client()

    @staticmethod
    def test_key(client):
        try:
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "This is a test"},
                    {"role": "user", "content": "this is a test"}
                ],
                temperature=0.1,
                max_tokens=5
            )
            return True
        except:
            return False

    def ask(self, question: str):
        print("Asking question: ", question)
        print("Client type: ", self.client_type)

        if self.client_type == "openai":
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a FAQ assistant."
                                                      "Your answer should be clear and straightforward."
                                                      "Do not include any unnecessary information."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.1,
                    max_tokens=100
                )
                return {"source": "openai",
                        "matched_question": "N/A",
                        "answer": response.choices[0].message.content}
            except openai.OpenAIError as e:  # handles RateLimit, Authentication, PermissionDenied, NotFound, etc
                print(f"Error from Openai side: {e}. Using the local model")
                self.switch_local()
                return self.ask(question)

        else:
            print("Using local model")
            return {"source": f"local-{OLLAMA_MODEL}",
                    "matched_question": "N/A",
                    "answer": self.client.invoke({"input": question})}

    def init_client(self):
        client = openai.OpenAI(api_key=api_key)

        if not self.test_key(client):
            model = Ollama(model=OLLAMA_MODEL, base_url=f"http://{OLLAMA_HOST}:11434")
            prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a FAQ assistant."
                               "Your answer should be clear and straightforward."
                               "Do not include any unnecessary information."),
                    ("user", "{input}")
                ])
            parser = StrOutputParser()
            client = prompt | model | parser
            client_type = "local"
            print("Invalid API key. Using local model instead.")
        else:
            client_type = "openai"
            print("Successfully connected to openai server")

        return client_type, client

    def register_key(self, key):
        if self.client_type == "local":
            client = openai.OpenAI(api_key=key)
            if self.test_key(client):
                self.client = client
                self.client_type = "openai"
                print("Successfully connected to openai server")
                return True
            else:
                print("Invalid API key. Using local model instead.")
                return False

    def switch_local(self):
        model = Ollama(model=OLLAMA_MODEL, base_url=f"http://{OLLAMA_HOST}:11434")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a FAQ assistant."
                       "Your answer should be clear and straightforward."
                       "Do not include any unnecessary information."),
            ("user", "{input}")
        ])
        parser = StrOutputParser()
        self.client = prompt | model | parser
        self.client_type = "local"
        print("Switched to local model")


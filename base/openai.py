from openai import OpenAI
from config import api_key
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


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
        else:
            print("Using local model")
            return {"source": "local-orca-mini",
                    "matched_question": "N/A",
                    "answer": self.client.invoke({"input": question})}

    def init_client(self):
        client = OpenAI(api_key=api_key)

        if not self.test_key(client):
            model = Ollama(model="orca-mini", base_url="http://172.16.200.12:11434")
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
            self.client = OpenAI(api_key=key)
            if self.test_key(self.client):
                self.client_type = "openai"
                print("Successfully connected to openai server")
                return True
            else:
                print("Invalid API key. Using local model instead.")
                return False

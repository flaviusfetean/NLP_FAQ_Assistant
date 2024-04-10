from openai import OpenAI
from config import api_key


class Assistant:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)

    def ask(self, question: str):
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
        return response.choices[0].message.content

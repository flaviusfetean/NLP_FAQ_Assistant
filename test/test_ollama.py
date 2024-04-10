from langchain_community.llms import Ollama

ollama = Ollama(model='orca-mini')


def main():
    queries = ["Say hi", "Write a C++ program which finds whether a number read from console is a power of 2 or not",
               "What is the difference between a compiler and an interpreter?"]
    for query in queries:
        for chunk in ollama.stream(query):
            print(chunk, end='')


if __name__ == "__main__":
    main()

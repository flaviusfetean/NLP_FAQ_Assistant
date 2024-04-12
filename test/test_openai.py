from base.openai import Assistant


def test_retrieval():
    assistant = Assistant()
    print(assistant.ask("Hello"))
    print(assistant.ask("What is the capital of France?"))
    print(assistant.ask("How can I change my password?"))


def main():
    test_retrieval()


if __name__ == "__main__":
    main()

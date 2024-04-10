from base.retrieve import *
from base.openai import *


def test_closest_match():
    test_query_list = [
        "How do I change my profile information?",
        "How can I retrieve lost data from my account?",
        "How do I go back to default account settings?",
        "What makes a good password?",
        "How can I change the password?",
        "How can I change the password",  # apparently the deletion of a question mark breaks the similarity for orca-mini
        "How to prepare for a job interview?",
        "What to do if I forget my password?"
    ]

    for query in test_query_list:
        print(get_closest_match(query))


def test_openai():
    assistant = Assistant()
    response = assistant.ask("How to change the password?")
    print(response)


def main():
    test_closest_match()
    #test_openai()


if __name__ == "__main__":
    main()

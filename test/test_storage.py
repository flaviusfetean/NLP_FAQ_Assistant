from storage.storage import *


def test_init_db():
    db = Database()

    queries = {"How do I change my profile information?",
               "what to do if my account is compromised?"}

    for query in queries:

        print("-" * 120)
        print("-" * 120)
        print("Query: ", query)

        answers = db.query_by_similarity(query, 3)

        for answer, score in answers:
            print("-" * 80)
            print("Score: ", score)
            print(answer.metadata['answer'])
            print("-" * 80)

    assert True


def main():
    test_init_db()


if __name__ == "__main__":
    main()

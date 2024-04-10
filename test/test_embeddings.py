from embeddings.embeddings import *


def test_query_similarity():

    test_pair_list = [
        ("I am testing with two equal sentences", "I am testing with two equal sentences"),
        ("I am testing with two slightly different sentences", "I am testing with two slightly modified sentences"),
        ("I am testing using quite different sentences", "I use modified enough versions of same thing"),
        ("These two sentences are totally different from each other", "The goal in football is to score more points than the other team")
    ]

    for pair in test_pair_list:
        print(get_query_similarity(embedding_model.embed_query(pair[0]), pair[1]))


def test_closest_match():
    test_query_list = [
        "How do I change my profile information?",
        "How can I retrieve lost data from my account?",
        "How do I go back to default account settings?",
        "What makes a good password?",
        "How to prepare for a job interview?"
    ]

    for query in test_query_list:
        print(get_closest_match(query))


def main():
    test_query_similarity()
    test_closest_match()


if __name__ == "__main__":
    main()

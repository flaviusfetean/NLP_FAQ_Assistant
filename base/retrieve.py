from storage.storage import Database
from base.openai import Assistant

db = Database()
assistant = Assistant()
SIMILARITY_THRESHOLD = 0.25

def get_closest_match(query: str):
    query = query.strip()
    answer, score = db.query_by_similarity(query, 1)[0]

    if score < SIMILARITY_THRESHOLD:
        return answer.metadata['answer']
    else:
        if query[-1] != "?":  # if no match is found, try to add or remove question mark,
            query += "?"      # as the question mark has a big impact on the embeddings and subsequently, similarity
        else:
            query = query[:-1]
        answer, score = db.query_by_similarity(query, 1)[0]
        if score < SIMILARITY_THRESHOLD:
            return answer.metadata['answer']

    #TODO: Insert the answer into the database if no match is found
    return assistant.ask(query)

from storage.storage import Database
from base.openai import Assistant

db = Database()
assistant = Assistant()

SIMILARITY_THRESHOLD = 0.2


def get_closest_match(query: str):
    print("Searching for closest match to: ", query)
    query = query.strip()
    try:
        answer, score = db.query_by_similarity(query, 1)[0]
    except IndexError:
        assistant_response = assistant.ask(query)
        db.insert(query, assistant_response['answer'])
        return assistant_response

    if score < SIMILARITY_THRESHOLD:
        return {"source": "local",
                "matched_question": answer.page_content,
                "answer": answer.metadata['answer']}
    else: #modify question mark status
        query_chg = query[:-1] if query[-1] == '?' else query[:] + '?'
        answer, score = db.query_by_similarity(query_chg, 1)[0]
        if score < SIMILARITY_THRESHOLD:
            return {"source": "local",
                    "matched_question": answer.page_content,
                    "answer": answer.metadata['answer']}

    print("No match found for: ", query)
    print("Forwarding to assistant")

    assistant_response = assistant.ask(query)
    db.insert(query, assistant_response['answer'])
    return assistant_response

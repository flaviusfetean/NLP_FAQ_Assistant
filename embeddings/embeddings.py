from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from storage.storage import Database
import numpy as np
import config

db = Database()


#embedding_model = OpenAIEmbeddings(api_key='api_key')
#embedding_model = OllamaEmbeddings(model='orca-mini')


def get_closest_match(query: str):
    answer, score = db.query_by_similarity(query, 1)[0]

    if score < config.SIMILARITY_THRESHOLD:
        return answer.metadata['answer']
    else:
        return "No match found"

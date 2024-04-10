from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from storage.storage import from_json_as_list
import numpy as np

#embedding_model = OpenAIEmbeddings(api_key='')
embedding_model = OllamaEmbeddings(model='orca-mini')


def get_query_similarity(embedding, target_query: str):
    return cosine_similarity([embedding], [embedding_model.embed_query(target_query)])[0][0]


def get_closest_match(query: str):
    query_embedding = embedding_model.embed_query(query)

    faq_list = from_json_as_list()
    similarities = [get_query_similarity(query_embedding, q['question']) for q in faq_list]
    max_sim_index = np.argmax(similarities)
    print(max(similarities))

    if max(similarities) < 0.5:
        return "I am sorry, the question you provided is too complicated for me, please contact a human expert."

    return faq_list[max_sim_index]['answer']
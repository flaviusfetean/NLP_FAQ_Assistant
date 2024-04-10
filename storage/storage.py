from langchain_community.vectorstores import PGVector
from langchain_community.document_loaders import JSONLoader, DataFrameLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores.pgvector import DistanceStrategy
import json
import pandas as pd
import os


class Database:

    COLLECTION_NAME = "questions"
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
        host=os.environ.get("PGVECTOR_HOST", "localhost"),
        port=int(os.environ.get("PGVECTOR_PORT", "5432")),
        database=os.environ.get("PGVECTOR_DATABASE", "faqdb"),
        user=os.environ.get("PGVECTOR_USER", "postgres"),
        password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
    )

    def __init__(self):
        self.embedding_model = OllamaEmbeddings(model='orca-mini')
        if os.path.exists(r"D:\GitHub\NLP_FAQ_Assistant\storage\db_init_status.txt"):
            with open(r"D:\GitHub\NLP_FAQ_Assistant\storage\db_init_status.txt", 'r') as f:
                init_status = f.readline()
        else:
            init_status = "NOT_INITIALIZED"

        if init_status == "INITIALIZED":
            self.db = PGVector(
                embedding_function=self.embedding_model,
                collection_name=self.COLLECTION_NAME,
                connection_string=self.CONNECTION_STRING
            )
        else:
            self.create_db()
            with open(r"D:\GitHub\NLP_FAQ_Assistant\storage\db_init_status.txt", 'w') as f:
                f.write("INITIALIZED")

    def create_db(self):
        df = pd.read_csv(r"D:\GitHub\NLP_FAQ_Assistant\storage\FAQ.csv", delimiter=';')
        loader = DataFrameLoader(df, page_content_column="question")
        docs = loader.load()

        self.db = PGVector.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            collection_name="questions",
            distance_strategy=DistanceStrategy.COSINE,
            connection_string=self.CONNECTION_STRING,
            pre_delete_collection=True)

    def query_by_similarity(self, query: str, top_k: int = 1):
        return self.db.similarity_search_with_score(query, top_k)


def from_json_as_list():
    db = open(r"D:\GitHub\NLP_FAQ_Assistant\storage\FAQ.json", 'r')
    json_data = json.load(db)
    return json_data


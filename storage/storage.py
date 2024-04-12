from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.docstore.document import Document
import pandas as pd
import psycopg2
import time
import os

PGVECTOR_DRIVER = os.environ.get("PGVECTOR_DRIVER", "psycopg2")
PGVECTOR_HOST = os.environ.get("PGVECTOR_HOST", "172.16.200.12")
PGVECTOR_PORT = os.environ.get("PGVECTOR_PORT", "5432")
PGVECTOR_DATABASE = os.environ.get("PGVECTOR_DATABASE", "faqdb")
PGVECTOR_USER = os.environ.get("PGVECTOR_USER", "postgres")
PGVECTOR_PASSWORD = os.environ.get("PGVECTOR_PASSWORD", "postgres")

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "172.16.200.13")


class Database:

    COLLECTION_NAME = "questions"
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=PGVECTOR_DRIVER,
        host=PGVECTOR_HOST,
        port=int(PGVECTOR_PORT),
        database=PGVECTOR_DATABASE,
        user=PGVECTOR_USER,
        password=PGVECTOR_PASSWORD
    )

    def __init__(self):
        self.wait_for_db_to_start()
        self.create_database_if_not_exists()
        self.create_extension_if_not_exists()

        self.embedding_model = OllamaEmbeddings(model='orca-mini', base_url=f"http://{OLLAMA_HOST}:11434")
        self.populate_db_if_not_populated()

    def wait_for_db_to_start(self):
        conn = None
        while not conn:
            try:
                conn = psycopg2.connect(
                    dbname='postgres',
                    user=PGVECTOR_USER,
                    password=PGVECTOR_PASSWORD,
                    host=PGVECTOR_HOST,
                    port=PGVECTOR_PORT
                )
                print("Database connection successful")
            except psycopg2.OperationalError as e:
                print(e)
                time.sleep(5)

    def create_database_if_not_exists(self):
        conn = psycopg2.connect(
            dbname='postgres',
            user=PGVECTOR_USER,
            password=PGVECTOR_PASSWORD,
            host=PGVECTOR_HOST,
            port=PGVECTOR_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # create faqdb if it does not exist
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{PGVECTOR_DATABASE}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {PGVECTOR_DATABASE}')
            print(f"Successfully created database {PGVECTOR_DATABASE}")
        else:
            print(f"Database {PGVECTOR_DATABASE} already exists. Skipping creation.")
        cur.close()
        conn.close()

    def create_extension_if_not_exists(self):
        conn = psycopg2.connect(
            dbname=PGVECTOR_DATABASE,
            user=PGVECTOR_USER,
            password=PGVECTOR_PASSWORD,
            host=PGVECTOR_HOST,
            port=PGVECTOR_PORT
        )
        cur = conn.cursor()

        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
        cur.close()
        conn.close()

    def populate_db_if_not_populated(self):
        # populate faqdb if it is empty
        try:
            self.db = PGVector(
                embedding_function=self.embedding_model,
                collection_name=self.COLLECTION_NAME,
                connection_string=self.CONNECTION_STRING
            )
            sample = self.db.similarity_search("Test", 1)[0]
            print(f"Database {PGVECTOR_DATABASE} already populated. Skipping population.")
        except IndexError:
            self.create_db()
            print(f"Successfully populated database {PGVECTOR_DATABASE}")

    def create_db(self):
        print("Populating database. This may take some time.")
        df = pd.read_csv(r"./storage/FAQ.csv", delimiter=';')
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

    def insert(self, question: str, answer: str):
        print("Inserting new question and answer into database")
        entry = Document(page_content=question, metadata={"answer": answer})
        self.db.add_documents([entry])

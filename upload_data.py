from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import GCSFileLoader
from langchain.text_splitter import CharacterTextSplitter

import names
import random
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()


def process_data(project_name, bucket, blob_name):
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free"
    )
    index_name = "testelon"
    embeddings = OpenAIEmbeddings()

    def load_pdf(file_path):
        return PyPDFLoader(file_path)

    loader = GCSFileLoader(
        project_name=project_name, bucket=bucket, blob=blob_name, loader_func=load_pdf
    )
    pages = loader.load_and_split()

    text_splitter = CharacterTextSplitter(
        chunk_size=500, chunk_overlap=20, separator="\n"
    )
    texts = text_splitter.split_documents(documents=pages)

    random_name = names.get_full_name()
    random_name = random_name + str(random.randrange(1, 500))
    Pinecone.from_documents(
        documents=texts,
        embedding=embeddings,
        index_name=index_name,
        namespace=random_name,
    )

    return random_name

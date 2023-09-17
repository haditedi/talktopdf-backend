from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import GCSFileLoader
from helper import delete_after_delay

import names
import random
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

def process_data(project_name, bucket, blob_name):
    # this function also handle deletion
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free"
    )
    index_name = "testelon"
    embeddings = OpenAIEmbeddings()

    def load_pdf(file_path):
        return PyPDFLoader(file_path)

    loader = GCSFileLoader(project_name=project_name, bucket=bucket, blob=blob_name, loader_func=load_pdf)
    # loader = PyPDFLoader(param)
    pages = loader.load_and_split()
    # print("PAGES",pages)
    print("LOADER", pages)
    text_splitter = CharacterTextSplitter(
        chunk_size=500, chunk_overlap=20, separator="\n"
    )
    texts = text_splitter.split_documents(documents=pages)
    # print("TEXTS",texts)
    print(len(texts))
    random_name = names.get_full_name()
    random_name = random_name + str(random.randrange(1,500))
    print(random_name)
    Pinecone.from_documents(
        documents=texts, embedding=embeddings, index_name=index_name, namespace=random_name
    )
    # delete_after_delay("testelon", random_name, param, 30)
    
    return random_name
   

# process_data("credit.pdf")

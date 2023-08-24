from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from helper import delete_after_delay

import names
import random
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

def process_data(param):
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free"
    )
    index_name = "testelon"
    embeddings = OpenAIEmbeddings()

    loader = PyPDFLoader(param)
    pages = loader.load_and_split()
    # print("PAGES",pages)
    text_splitter = CharacterTextSplitter(
        chunk_size=500, chunk_overlap=20, separator="\n"
    )
    texts = text_splitter.split_documents(documents=pages)
    # print("TEXTS",texts)
    print(len(texts))
    random_name = names.get_full_name()
    random_name = random_name + str(random.randrange(1,500))
    print(random_name)
    doc_store = Pinecone.from_documents(
        documents=texts, embedding=embeddings, index_name=index_name, namespace=random_name
    )
    # delete_after_delay("testelon2", random_name, param, 30)
    
    return random_name
   

# process_data("credit.pdf")

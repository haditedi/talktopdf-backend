from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import GCSFileLoader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

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


def process_url_data(url):
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free"
    )
    index_name = "testelon"
    embeddings = OpenAIEmbeddings()
    loader = RecursiveUrlLoader(
        url=url, max_depth=5, extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()
    print("LENGTH LIST", len(docs))

    seen = set()
    newlist = []
    for i in docs:
        key = i.page_content
        if key in seen:
            continue
        seen.add(key)
        item = " ".join(i.page_content.split())
        i.page_content = item
        i.metadata = {}
        newlist.append(i)
    # print("LENGTH NEW LIST", len(newlist))
    # print("NEWLIST", newlist[0])
    # print("NEWLIST", newlist[1])
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(documents=newlist)
    if len(texts) > 400:
        return {"message": "Data too big,,,", "namespace": ""}

    print("LENGHT TEXT", len(texts))

    random_name = names.get_full_name()
    random_name = random_name + str(random.randrange(1, 500))
    print(random_name)

    try:
        Pinecone.from_documents(
            documents=texts,
            embedding=embeddings,
            index_name=index_name,
            namespace=random_name,
        )
    except Exception as e:
        print("ERROR", e)
        return e

    return {"namespace": random_name, "message": "ok"}


# process_url_data("https://www.byronhotel.co.uk")

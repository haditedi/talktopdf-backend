from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter

import pinecone
from dotenv import load_dotenv
import os
import openai


load_dotenv()


def process_data(param):
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free"
    )
    index_name = "testelon2"
    embeddings = OpenAIEmbeddings()

    loader = UnstructuredPDFLoader(param)
    loader = PyPDFLoader(param)
    pages = loader.load_and_split()
    # print(pages)
    text_splitter = CharacterTextSplitter(
        chunk_size=500, chunk_overlap=20, separator="\n"
    )
    texts = text_splitter.split_documents(documents=pages)
    # print(texts)
    print(len(texts))
    # loader = TextLoader(param,autodetect_encoding=True)
    # documents = loader.load()
    # documents = documents[0].page_content
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20, separator="\n")
    # texts = text_splitter.split_documents(documents=documents)
    # print("Length", documents[0].page_content)
    doc_store = Pinecone.from_documents(
        documents=texts, embedding=embeddings, index_name=index_name, namespace="olala"
    )
    # qa = RetrievalQA.from_chain_type(llm = OpenAI(), chain_type="stuff", retriever=doc_store.as_retriever())


process_data("event.pdf")

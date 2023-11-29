from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")


def chat_pdf(query, namespace):
    embeddings = OpenAIEmbeddings()
    index_name = "testelon"

    retriever = Pinecone.from_existing_index(
        embedding=embeddings, index_name=index_name, namespace=namespace
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever.as_retriever(), verbose=True, memory=memory
    )

    result = chain({"question": query})
    print(result["answer"])
    return result["answer"]


# chat_pdf("where is byron hotel", "Steven Sokol423")

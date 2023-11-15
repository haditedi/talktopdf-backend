import pinecone
from dotenv import load_dotenv
import os
import time

load_dotenv()

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")


def delete_namespace(index, namespace):
    try:
        index = pinecone.Index(index)
        index.delete(delete_all=True, namespace=namespace)
        print(f"{namespace} namespace deleted")
    except Exception as e:
        print("ERROR delete namespace ", e)


def delete_pdf(path_location):
    if os.path.exists(path_location):
        os.remove(path_location)
        print("PATH DELETED")
    else:
        print("PATH NOT EXIST")


def delete_after_delay(index, namespace, delay_seconds):
    print(f"Deleting {namespace} after {delay_seconds} seconds")
    time.sleep(delay_seconds)
    delete_namespace(index, namespace)


def delete_one(index, namespace):
    index = pinecone.Index(index)
    try:
        index.delete(delete_all=True, namespace=namespace)
        print(f"{namespace} deleted")
    except Exception as e:
        print("something went wrong ", e)


def create_index(name):
    try:
        pinecone.create_index(name, dimension=1536, metric="euclidean")
        print(f"{name} created")
    except Exception as e:
        print("something went wrong ", e)


def delete_index(name):
    try:
        pinecone.delete_index(name)
        print(f"{name} deleted")
    except Exception as e:
        print("something went wrong ", e)


def allowed_file(filename):
    allowed_extensions = {"pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# delete_index("testelon2")
# delete_one("testelon", "Patricia Devito175")
# delete_after_delay("testelon2", "Paul Brunette357",1)
# create_index("testelon")
def delete_all_namespace(index):
    index = pinecone.Index(index)
    namespaces = index.describe_index_stats().namespaces
    for x in namespaces:
        index.delete(delete_all=True, namespace=x)
        print(f"{x} namespace deleted")


# delete_all_namespace("testelon")

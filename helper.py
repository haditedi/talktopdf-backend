import pinecone
from dotenv import load_dotenv
from storageG import delete_blob
import os
import asyncio

load_dotenv()

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")

def delete_namespace(index,namespace):
    try:
        index = pinecone.Index(index)
        index.delete(delete_all=True, namespace=namespace)
        print(f"{namespace} namespace deleted")
    except Exception as e:
        print("ERROR delete namespace ",e)

def delete_pdf(path_location):
    if os.path.exists(path_location):
        os.remove(path_location)
        print("PATH DELETED")
    else:
        print("PATH NOT EXIST")

import threading
import time

def delete_after_delay(index, namespace, bucket_name,blob_name, delay_seconds):
    print(f"Deleting {namespace} after {delay_seconds} seconds")
    time.sleep(delay_seconds)
    delete_blob(bucket_name, blob_name)
    delete_namespace(index, namespace)

def delete_one(index, namespace):
    index = pinecone.Index(index)
    try:
        index.delete(delete_all=True, namespace=namespace)
        print(f"{namespace} deleted")
    except Exception as e:
        print("something went wrong ",e)

def create_index(name):
    try:
        pinecone.create_index(name, dimension=1536, metric="euclidean")
        print(f"{name} created")
    except Exception as e:
        print("something went wrong ",e)

def delete_index(name):
    try:
        pinecone.delete_index(name)
        print(f"{name} deleted")
    except Exception as e:
        print("something went wrong ",e)
    

def allowed_file(filename):
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# delete_index("testelon2")
# delete_one("testelon", "Le Needham357")
# delete_after_delay("testelon2", "Paul Brunette357",1)
# create_index("testelon")



# async def async_function():
#     print("Start async_function")
#     time.sleep(2)
#     # await asyncio.sleep(2)  # Simulate some asynchronous task
#     print("Async_function completed")

# async def main():
#     print("Main program start")
#     asyncio.create_task(async_function())
#     print("Main program end")

# asyncio.run(main())






import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")

def delete_namespace(index,namespace):
    index = pinecone.Index(index)
    index.delete(delete_all=True, namespace=namespace)

import threading
import time

def delete_after_delay(index, namespace, delay_seconds):
    def delete_item():
        print(f"Deleting {namespace} after {delay_seconds} seconds")
        time.sleep(delay_seconds)
        delete_namespace(index, namespace)
        

        # Perform the deletion operation here
        # For example, you could delete a file, remove an item from a list, etc.
        # Replace the following line with the actual deletion operation

        # Example: Deleting a file
        # import os
        # os.remove(item_to_delete)

        # Example: Removing an item from a list
        # my_list.remove(item_to_delete)

    deletion_thread = threading.Thread(target=delete_item)
    deletion_thread.start()


def allowed_file(filename):
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



# delete_after_delay("testelon2", "Paul Brunette357",1)


from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from google.cloud import storage
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from pypdf import PdfReader
from dotenv import load_dotenv
from helper import allowed_file
from helper import delete_after_delay
from upload_data import process_data
from chat_pdf import chat_pdf
from storageG import upload_blob_from_stream
import os
import openai
import random
# import asyncio

load_dotenv()

BUCKET_NAME="talktopdf.appspot.com"
PUBLIC_BUCKET="https://storage.googleapis.com/talktopdf.appspot.com/"
INDEX="testelon"

app = Flask(__name__)

CORS(app)
# CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5173/"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def converse():
    if request.method == "POST":
        print("CONVERSE")
        data = request.json
        try:
            query = data["query"]  
            namespace = data["namespace"]
            print("QUERY", query)
            print("NAMESPACE",namespace)
        except Exception as e:
            return jsonify(e)
        print("NAMESPACE",namespace)
        if query != "" and namespace != "":
            result = chat_pdf(query, namespace)
            return jsonify({"content" : result, "status":"ok"})
        else:
            return {"content" : "something went wrong"}

@app.route("/upload", methods=["POST","GET"])
def upload():
    print("UPLOAD",request.files)
    if request.method == "POST":
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        
        if file.filename == '':
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            if secure_filename(file.filename):
                # path_location=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                # file.save(path_location)
                random_int = str(random.randrange(1,500))
                destination_filename = random_int+file.filename
                upload_blob_from_stream(BUCKET_NAME, file, destination_filename) 
                # upload_blob(BUCKET_NAME, path_location, file.filename)
                # bucket_url=f"{PUBLIC_BUCKET}{destination_filename}"
                print("URL",f"{PUBLIC_BUCKET}{destination_filename}")
                namespace = process_data(f"{PUBLIC_BUCKET}{destination_filename}")
                # delete_after_delay(INDEX,namespace,BUCKET_NAME,destination_filename,60*5)
                print("NAMESPACE",namespace)
                print("DESTINATION FILE NAME", destination_filename)  
                return {"message": "File uploaded successfully", "namespace": namespace, "destination_file_name":destination_filename, "status":"ok"}
        else:
            return {"error": "Invalid file format"}, 400

@app.route("/delete", methods=["POST"])
def delete():  
    data = request.json
    print("DELETE", data)
    try:     
        namespace = data["namespace"]
        destination_file_name = data["destinationFileName"]
        # print("QUERY", query)
        print("NAMESPACE",namespace)
        delete_after_delay(INDEX,namespace,BUCKET_NAME,destination_file_name,60*5)
        return jsonify()
    except Exception as e:
        return jsonify(e)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
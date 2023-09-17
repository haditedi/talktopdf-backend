from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from google.cloud import storage
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from helper import allowed_file
from helper import delete_after_delay, delete_all_namespace
from upload_data import process_data
from chat_pdf import chat_pdf
from storageG import upload_blob_from_stream, delete_blob
import os
import openai
import random
import logging

load_dotenv()

PROJECT_NAME="talktopdf"
BUCKET_NAME="talktopdf.appspot.com"
PUBLIC_BUCKET="https://storage.googleapis.com/talktopdf.appspot.com/"
INDEX="testelon"

app = Flask(__name__)

CORS(app)
# CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5173/"}})
# CORS(app, resources={r"/": {"origins": "https://talktopdf.vercel.app"}})
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def converse():
    if request.method == "GET":
        return {"status":"Error", "content":"error"},400
    if request.method == "POST":
        print("CONVERSE")
        data = request.json
        try:
            query = data["query"]  
            namespace = data["namespace"]
            print("QUERY", query)
            print("NAMESPACE",namespace)
            print("REQ",request.headers)
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
 
    if request.method == "POST":
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        extension = file.filename[-3:].lower()
        print("EXTENSION", extension)
        if extension != "pdf":
            print("FILE")
            return {"error":"PDF file only please"},400
        
        if file.filename == '':
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            if secure_filename(file.filename):
                # path_location=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                # file.save(path_location)
                random_int = str(random.randrange(1,500))
                destination_filename = random_int+file.filename
                upload_blob_from_stream(BUCKET_NAME, file, destination_filename) 
                # bucket_url=f"{PUBLIC_BUCKET}{destination_filename}"
                # print("URL",f"{PUBLIC_BUCKET}{destination_filename}")
                # namespace = process_data(f"{PUBLIC_BUCKET}{destination_filename}") 
                namespace = process_data(project_name=PROJECT_NAME, bucket=BUCKET_NAME,blob_name=destination_filename) 
                # delete_after_delay(INDEX,namespace,BUCKET_NAME,destination_filename,60*5)
                # delete_blob(BUCKET_NAME,destination_filename)
                print("NAMESPACE",namespace)
                print("DESTINATION FILE NAME", destination_filename)  
                return {"message": "File uploaded successfully", "namespace": namespace, "destination_file_name":destination_filename, "status":"ok"}
        else:
            return {"error": "Invalid file format"}, 400

@app.route("/delete", methods=["POST","GET"])
def delete():
    if request.method == "POST":
        return {"status":"Error", "content":"error"},400   
              
    if request.method == "GET":
        logging.info("DELETE /GET", request.headers)
        print(request.headers)
        if request.headers['X-Appengine-Cron'] == "true":
            delete_all_namespace(INDEX)
            print("TRUE")
        return {"status":"ok", "content": "deleted"},200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
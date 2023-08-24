from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from pypdf import PdfReader
from dotenv import load_dotenv
from helper import allowed_file
from upload_data import process_data
from chat_pdf import chat_pdf
import os
import openai

load_dotenv()

UPLOAD_FOLDER="./upload"
app = Flask(__name__)

# Configuration for file upload
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5173/"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def converse():
    if request.method == "POST":
        print("CONVERSE")
        data = request.json
        print("DATA",data)
        query = data["query"]
        print("QUERY",query)
        namespace = data["namespace"]
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
                path_location=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path_location) 
                namespace = process_data(path_location)
                print(namespace)
                  
                return {"message": "File uploaded successfully", "namespace": namespace, "status":"ok"}
        else:
            return {"error": "Invalid file format"}, 400
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
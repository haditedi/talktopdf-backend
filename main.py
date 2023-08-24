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

app = Flask(__name__)
# Configuration for file upload
CORS(app)

# CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5173/"}})
# app.config['UPLOAD_FOLDER'] = 'uploads'
# ALLOWED_EXTENSIONS = {'pdf'}

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/converse", methods=["GET"])
def converse():
    print("CONVERSE")
    data = request.json
    query = data["body"]
    result = chat_pdf(query, "William Peel305")

    return {"content" : result}

@app.route("/upload", methods=["POST","GET"])
def upload():
    print("UPLOAD",request.files)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        
        if file.filename == '':
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            if secure_filename(file.filename): 
                reader = PdfReader(file)
                result = [x.extract_text() for x in reader.pages]
                
                process_data(result)
                # print(len(reader.pages))
                # page = reader.pages[0]
                # print(page.extract_text())       
                return {"message": "File uploaded successfully","status":"ok"}
        else:
            return {"error": "Invalid file format"}, 400
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
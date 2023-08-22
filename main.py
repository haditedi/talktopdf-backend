from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from helper import allowed_file
import os
import openai

load_dotenv()

app = Flask(__name__)
# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/upload", methods=["POST","GET"])
def upload():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']
    
    if file.filename == '':
        return {"error": "No selected file"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)        
        return {"message": "File uploaded successfully"}, 200
    else:
        return {"error": "Invalid file format"}, 400
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
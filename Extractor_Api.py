# Flask Backend API: Upload Emails or Letters, Return CSV/JSON

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from email_extractor_backend import extract_emails, extract_letters, save_to_csv_and_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/extract/email", methods=["POST"])
def extract_email():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    start = int(data.get("start", 0))
    end = int(data.get("end", 1000))

    if not (email and password):
        return jsonify({"error": "Email and password required"}), 400

    results = extract_emails(email, password, start, end)

    if not results:
        return jsonify({"error": "No emails were extracted."}), 400

    output = save_to_csv_and_db(results)

    if not output:
        return jsonify({"error": "Failed to save outputs"}), 500

    csv_path, json_path, _ = output
    return jsonify({"message": f"Extracted {len(results)} emails", "csv": csv_path, "json": json_path})

@app.route("/extract/letter", methods=["POST"])
def extract_letter():
    files = request.files.getlist("files")
    file_paths = []

    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        file_paths.append(path)

    results = extract_letters(file_paths)
    csv_path, json_path, _ = save_to_csv_and_db(results)
    return jsonify({"message": f"Processed {len(results)} letters", "csv": csv_path, "json": json_path})

@app.route("/download/<file_type>")
def download_file(file_type):
    if file_type == "csv":
        return send_file("documents.csv", as_attachment=True)
    elif file_type == "json":
        return send_file("documents.json", as_attachment=True)
    else:
        return "Invalid file type", 400

if __name__ == "__main__":
    app.run(debug=True, port=5050)

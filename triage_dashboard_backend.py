# triage_dashboard_backend.py

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
import sqlite3
import uuid
from email_extractor_backend import classify_message, summarize_message, save_to_csv_and_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/triage/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(filepath)
        elif filename.endswith(".json"):
            df = pd.read_json(filepath)
        elif filename.endswith(".db"):
            conn = sqlite3.connect(filepath)
            df = pd.read_sql("SELECT * FROM documents", conn)
            conn.close()
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500

    triaged = []
    for _, row in df.iterrows():
        body = row.get("body", "")
        label, keywords, priority = classify_message(body)
        summary = summarize_message(body)

        triaged.append({
            **row.to_dict(),
            "label": label,
            "keywords": ", ".join(keywords),
            "priority": priority,
            "summary": summary
        })

    triaged_df = pd.DataFrame(triaged)
    csv_path, _, _ = save_to_csv_and_db(triaged)

    return jsonify({
        "message": f"Classified {len(triaged)} entries",
        "csv": csv_path,
        "data": triaged[:50]  # limit rows returned to frontend
    })

@app.route("/triage/download/csv")
def download_csv():
    return send_file("documents.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5051)

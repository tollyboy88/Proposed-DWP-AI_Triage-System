# email_extractor_backend.py

import imaplib
import email
import os
import json
import pandas as pd
import sqlite3
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import uuid

# -- Vulnerability Keywords and Labels --
KEYWORD_LABELS = {
    "terminal_illness": ["cancer", "chemotherapy", "terminal", "late-stage", "stroke"],
    "homelessness": ["homeless", "evicted", "no fixed address", "sleeping rough"],
    "mental_health": ["low", "can't cope", "depressed", "mental health", "struggling emotionally"],
    "disability_support": ["disabled", "disability", "carer", "autism"],
    "domestic_abuse": ["abuse", "unsafe", "fled", "violence"],
    "elderly_support": ["heating", "pensioner", "old", "75", "alone"],
    "bereavement_support": ["miscarriage", "lost parents", "bereaved"],
    "job_loss": ["lost my job", "redundant", "laid off"],
    "refugee_support": ["asylum", "refugee", "leave to remain"],
    "routine": ["bank details", "update", "confirm", "statement", "routine"]
}

# Set path if Tesseract is not in system PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def classify_message(text):
    label = "unclassified"
    found_keywords = []
    priority = "low"

    for key, words in KEYWORD_LABELS.items():
        for word in words:
            if word.lower() in text.lower():
                label = key
                found_keywords.append(word)
                priority = "high" if key != "routine" else "medium"

    return label, found_keywords, priority

def summarize_message(text):
    # Dummy summarizer (replace with LLM API or model if needed)
    summary = text[:300] + ("..." if len(text) > 300 else "")
    return summary

def extract_emails(user_email, app_password, start=0, end=100):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user_email, app_password)
    imap.select("inbox")

    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()[start:end]
    results = []

    for eid in email_ids:
        _, msg_data = imap.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"] or ""
        sender = msg["from"] or ""
        date = msg["date"] or ""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body += msg.get_payload(decode=True).decode(errors="ignore")

        label, keywords, priority = classify_message(body)
        summary = summarize_message(body)

        results.append({
            "source": "email",
            "subject": subject,
            "sender": sender,
            "date": date,
            "body": body,
            "summary": summary,
            "label": label,
            "keywords": ", ".join(keywords),
            "priority": priority
        })

    imap.logout()
    return results

def extract_letters(file_paths):
    results = []
    for path in file_paths:
        text = ""
        if path.lower().endswith(".pdf"):
            pages = convert_from_path(path)
            for page in pages:
                text += pytesseract.image_to_string(page)
        else:
            image = Image.open(path)
            text += pytesseract.image_to_string(image)

        label, keywords, priority = classify_message(text)
        summary = summarize_message(text)

        results.append({
            "source": "letter",
            "filename": os.path.basename(path),
            "body": text,
            "summary": summary,
            "label": label,
            "keywords": ", ".join(keywords),
            "priority": priority
        })
    return results

def save_to_csv_and_db(data):
    if not data:
        return None

    df = pd.DataFrame(data)
    csv_path = "documents.csv"
    json_path = "documents.json"
    db_path = "documents.db"

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    conn = sqlite3.connect(db_path)
    df.to_sql("documents", conn, if_exists="replace", index=False)
    conn.close()

    return csv_path, json_path, db_path

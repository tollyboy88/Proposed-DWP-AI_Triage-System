# Welcome to your DWP AI Triage & Document Intelligence System

## Project Info

**Overview**:
This project delivers a complete AI-powered document intake, classification, and triage solution built for DWP's use case. It consists of three main modules:

* Streamlit Upload & Threat Analysis Interface
* Flask API for Document Triage
* Frontend HTML Dashboard for Human-in-the-loop Review



## How can I edit this code?

You can use any of the following options:

### **Use your preferred IDE**

```sh
# Step 1: Clone the repository
 git clone <[YOUR_GIT_UR](https://github.com/tollyboy88/Proposed-DWP-AI_Triage-System)L>

# Step 2: Navigate to the project directory
 cd dwp-triage-system

# Step 3: Set up Python virtual environment
 python -m venv venv && source venv/bin/activate

# Step 4: Install required dependencies
 pip install -r requirements.txt

# Step 5: Start Flask API (for backend triage)
 cd backend && flask run --port=5051

# Step 6: Run Streamlit app (for media threat detection)
 cd ../streamlit_ui && streamlit run app.py

# Step 7: Open HTML frontend in browser
 open frontend/triage_dashboard_frontend.html
```

## Tools and Technologies Used

* **Python 3.10+**
* **Flask**: API for triage analysis and file uploads
* **Streamlit**: Interface for document/image/video/audio threat analysis
* **HTML + JavaScript**: Dashboard UI for results display
* **SQLite3** (Optional): Persistence layer

### AI/NLP/OCR Libraries Used:

* **spaCy**: Named Entity Recognition
* **Transformers**: LLM for classification, summarization
* **scikit-learn**: Vectorization, ROC-AUC, F1, confusion matrix
* **OpenCV**: Image preprocessing (if used)
* **Tesseract OCR**: Optical character recognition
* **Pandas** / **NumPy**: Data manipulation

## Key Features

* ✅ Document upload & parsing (PDF, DOCX, DB, JSON, etc.)
* ✅ Named Entity Recognition (NER) and keyword matching
* ✅ Human-in-the-loop dashboard
* ✅ Triage prediction (priority, label, risk)
* ✅ Custom hallucination, fairness and bias metrics
* ✅ Model evaluation: Accuracy, F1-score, Recall, ROC-AUC

## Deployment Options

* **Localhost**: Run backend on `localhost:5051`, frontend via `triage_dashboard_frontend.html`
* **Replit / Render / HuggingFace Spaces**: Fully compatible with Streamlit and Flask

## Folder Structure

```
root/
├── backend/                       # Flask app for triage API
│   ├── app.py
│   └── model_utils.py
├── streamlit_ui/                 # Streamlit media analysis
│   └── app.py
├── frontend/
│   └── triage_dashboard_frontend.html
├── data/                         # Sample files or datasets
├── requirements.txt
└── README.md                     # You're here
```

## How can I contribute?

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request ✅

---

## Questions or Feedback?

Please open an issue or contact the maintainers.
adebayoadetola96@yahoo.com

---

*This project was built with ❤️ to help DWP triage vulnerable cases with AI-powered transparency and fairness.*

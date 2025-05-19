from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS
import os
from pymongo import MongoClient
from umap import UMAP
import numpy as np
import logging
from backend_analysis_api import run_analysis  # Import your run_analysis function

app = Flask(__name__)
CORS(app)

# 🔹 MongoDB Connection Setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rasa"
COLLECTION_NAME = "conversations"

# 🔹 Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_all_patients_sessions():
    """
    Fetches all patients along with their session IDs from MongoDB.
    Transforms the result into the format:
      { id: <count>, name: <patient_name>, sessions: [<session_id>, ...] }
    """
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            pipeline = [
                {
                    "$group": {
                        "_id": "$patient_id",
                        "sessions": {"$addToSet": "$session_id"}
                    }
                }
            ]

            result = list(collection.aggregate(pipeline))
            # Transform result: assign incremental id and use patient name
            patients_sessions = []
            for count, entry in enumerate(result, start=1):
                patients_sessions.append({
                    "id": count,
                    "name": entry["_id"],
                    "sessions": sorted(entry["sessions"])
                })

            return patients_sessions

    except Exception as e:
        app.logger.error(f"Error fetching patient sessions: {e}")
        return []

@app.route("/get-patients-sessions", methods=["GET"])
def get_patients_sessions():
    patients_sessions = fetch_all_patients_sessions()
    return jsonify(patients_sessions)

@app.route("/get-report", methods=["POST"])
def get_report():
    data = request.get_json()
    patient_id = data.get("patient")
    session_id = data.get("session")

    if not patient_id or not session_id:
        return jsonify({"error": "Patient and session required"}), 400

    try:
        with MongoClient(MONGO_URI) as client:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            patient_data = collection.find_one({"patient_id": patient_id, "session_id": session_id})

            if not patient_data:
                logger.warning(f"⚠️ No data found for Patient ID: {patient_id}, Session ID: {session_id}")
                return jsonify({"error": "No data found for this patient and session"}), 404

            entire_convo=[msg["text"] for msg in patient_data.get("messages", [])]
            messages = [msg["text"] for msg in patient_data.get("messages", []) if msg.get("sender") == "patient"]

            logger.info(f"✅ Fetched {len(messages)} messages for Patient ID: {patient_id}, Session ID: {session_id}")

    except Exception as e:
        logger.error(f"❌ Error fetching patient data: {e}")
        return jsonify({"error": "Database error"}), 500

    # Ensure `run_analysis` is always called properly
    report = run_analysis(patient_id, session_id, messages)
    report["entire_convo"]=entire_convo

    if report is None:
        return jsonify({"error": "Failed to generate report"}), 500

    return jsonify(report)

@app.route("/static/<filename>")
def get_static_file(filename):
    """
    Serves static image & interactive HTML files.
    """
    
    path = os.path.join('E:\\ai_psychotherapist\\',filename)
    if os.path.exists(path):
        if filename.endswith(".png"):
            return send_file(path, mimetype="image/png")
        elif filename.endswith(".html"):
            return send_file(path, mimetype="text/html")
    return jsonify({"error": "File not found"}), 404


@app.route("/interactive/<filename>")
def get_interactive(filename):
    """
    Serves interactive HTML files (like the interactive sentiment analysis plot).
    Files are assumed to be in the static/html directory.
    """
    html_dir = os.path.join(os.getcwd(), "static", "html")
    path = os.path.join(html_dir, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="text/html")
    return jsonify({"error": "Interactive file not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

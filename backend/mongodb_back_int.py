import os
import torch
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import logging
from pymongo import MongoClient  # 🔹 MongoDB Integration
from backend_analysis_api import run_analysis  # 🔹 Importing the analysis functions

# 🔹 MongoDB Connection Setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rasa"
COLLECTION_NAME = "conversations"

# 🔹 Check GPU Availability
DEVICE = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'GPU' if DEVICE == 0 else 'CPU'}")

# 🔹 Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
# 🔹 Fetch Patient Data from MongoDB
############################################
def fetch_patient_data(patient_id):
    """
    Fetches patient data (session ID and messages) from MongoDB.
    """
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            # 🔹 Get the most recent session for the patient
            patient_data = collection.find_one({"patient_id": patient_id}, sort=[("session_id", -1)])

            if not patient_data:
                logger.warning(f"⚠️ No data found for Patient ID: {patient_id}")
                return None, None, []

            session_id = patient_data.get("session_id", "1")
            messages = [msg["text"] for msg in patient_data.get("messages", []) if msg.get("sender") == "patient"]

            logger.info(f"✅ Fetched data for Patient ID: {patient_id}, Session ID: {session_id}, Messages: {len(messages)}")

            return patient_id, session_id, messages

    except Exception as e:
        logger.error(f"❌ Error fetching patient data: {e}")
        return None, None, []
    
def fetch_all_patients_sessions():
    """
    Fetches all patients along with their session IDs from MongoDB.
    """
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            # 🔹 Get all patients and their session IDs
            pipeline = [
                {
                    "$group": {
                        "_id": "$patient_id",
                        "sessions": {"$addToSet": "$session_id"}
                    }
                }
            ]

            result = list(collection.aggregate(pipeline))  # Force full iteration

            # Convert result to dictionary format
            patients_sessions = {entry["_id"]: sorted(entry["sessions"]) for entry in result}

            logger.info(f"✅ Retrieved sessions for {len(patients_sessions)} patients")
            
            # 🔹 Debugging: Log all retrieved patients
            for patient, sessions in patients_sessions.items():
                logger.debug(f"👤 Patient: {patient}, Sessions: {sessions}")

            return patients_sessions

    except Exception as e:
        logger.error(f"❌ Error fetching patient sessions: {e}")
        return {}


############################################
# 🔹 Main Execution: Fetch Data & Run Analysis
############################################
if __name__ == "__main__":
    patient_id = "test_userss"  # Change this dynamically in production
    patient, session, user_messages = fetch_patient_data(patient_id)

    #if patient and session and user_messages:
        #result = run_analysis(patient, session, user_messages)

        #print("\n🔹 **Final Analysis Results:**")
        #for key, value in result.items():
            #print(f"\n🔹 {key.upper()}:")
            #if isinstance(value, dict):
                #for sub_key, sub_value in value.items():
                    #print(f"  {sub_key}: {sub_value}")
            #else:
                #print(f"  {value}")
    #else:
        #print("⚠️ No valid patient data found. Analysis could not be performed.")
    print(fetch_all_patients_sessions())

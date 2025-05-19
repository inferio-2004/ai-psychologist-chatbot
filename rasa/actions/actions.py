from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from pymongo import MongoClient
import os

# MongoDB Connection Setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rasa"
COLLECTION_NAME = "conversations"

class ActionStorePatientID(Action):
    def name(self):
        return "action_store_patient_id"

    def run(self, dispatcher, tracker, domain):
        """
        Stores the patient_id that was sent from the frontend when the chat starts.
        The frontend must send this ID as the sender parameter in the API request.
        """
        patient_id = tracker.sender_id  # Patient ID is sent as 'sender' from frontend

        # Store the patient ID in the slot so it's accessible throughout the session
        return [SlotSet("patient_id", patient_id)]


class ActionLogConversation(Action):
    def name(self):
        return "action_log_conversation"

    def run(self, dispatcher, tracker, domain):
        """
        Logs the conversation messages under the patient's ID in MongoDB.
        """
        patient_id = tracker.get_slot("patient_id") or tracker.sender_id  # Ensure we use patient_id

        if not patient_id:
            dispatcher.utter_message("Patient ID not found. Unable to log conversation.")
            return []

        conversation_data = []
        for event in tracker.events:
            if event.get("event") == "user":
                conversation_data.append({
                    "timestamp": event["timestamp"],
                    "text": event["text"],
                    "intent": event.get("parse_data", {}).get("intent", {}).get("name"),
                })
            elif event.get("event") == "bot":  # Capturing bot responses
                conversation_data.append({
                    "timestamp": event["timestamp"],
                    "text": event.get("text"),
                    "sender": "bot"
                })

        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Store messages under the patient's record
        collection.update_one(
            {"patient_id": patient_id},
            {"$push": {"messages": {"$each": conversation_data}}},
            upsert=True  # Create a new record if patient_id doesn't exist
        )

        dispatcher.utter_message("Your conversation has been logged.")
        return []
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Ai_psych"
COLLECTION_NAME = "conversations"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Insert a test document
collection.insert_one({"message": "Hello, MongoDB!"})

print("Inserted a document successfully!")

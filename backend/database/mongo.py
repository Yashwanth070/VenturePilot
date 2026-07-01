from pymongo import MongoClient
import os
import bcrypt
import datetime
from bson.objectid import ObjectId

class Database:
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.client = None
        self.db = None

    def connect(self):
        if self.uri and self.uri != "your_mongodb_uri_here":
            try:
                self.client = MongoClient(self.uri)
                self.db = self.client['venturepilot']
                print("Connected to MongoDB Atlas")
            except Exception as e:
                print(f"MongoDB connection error: {e}")
        else:
            print("Running without MongoDB (Mock mode)")

    def is_connected(self):
        return self.db is not None

    # User Auth
    def create_user(self, email, password, name):
        if not self.is_connected(): return {"_id": "mock_id", "email": email, "name": name}
        
        existing = self.db.users.find_one({"email": email})
        if existing:
            return None
            
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            "email": email,
            "password": hashed,
            "name": name,
            "created_at": datetime.datetime.utcnow()
        }
        result = self.db.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        del user['password']
        return user

    def authenticate_user(self, email, password):
        if not self.is_connected(): return {"_id": "mock_id", "email": email, "name": "Mock User"}
        
        user = self.db.users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user['_id'] = str(user['_id'])
            del user['password']
            return user
        return None

    # Save Analyses
    def save_analysis(self, collection_name, user_id, data):
        if not self.is_connected(): return "mock_id"
        
        data['user_id'] = user_id
        data['created_at'] = datetime.datetime.utcnow()
        result = self.db[collection_name].insert_one(data)
        return str(result.inserted_id)

    def get_analyses(self, collection_name, user_id):
        if not self.is_connected(): return []
        
        cursor = self.db[collection_name].find({"user_id": user_id}).sort("created_at", -1)
        results = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            results.append(doc)
        return results

db = Database()

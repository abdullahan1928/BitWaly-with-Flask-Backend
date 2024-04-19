from app import mongo
from datetime import datetime
from bson.objectid import ObjectId

class User:
    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.utcnow()
        self.last_login = None  # Set to None initially

    @staticmethod
    def to_json(user):
        return {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        }

    def save(self):
        users_collection = mongo.db.users
        users_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        users_collection = mongo.db.users
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_by_id(id: str):
        users_collection = mongo.db.users
        try:
            return users_collection.find_one({"_id": ObjectId(id)})
        except:
            return None

    @staticmethod
    def update_last_login(email, last_login):
        users_collection = mongo.db.users
        users_collection.update_one(
            {"email": email}, {"$set": {"last_login": last_login}})

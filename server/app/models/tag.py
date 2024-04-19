from app import mongo
from bson.objectid import ObjectId


class Tag:
    def __init__(self, user, urls, name):
        self.user = user
        self.urls = urls
        self.name = name

    def save(self):
        tags_collection = mongo.db.tags
        tags_collection.insert_one(self.__dict__)

    @staticmethod
    def create_tag(user_id, url, tag_name):
        tag_instance = Tag(user=user_id, urls=[url], name=tag_name)
        tag_instance.save()
        return tag_instance.__dict__

    @staticmethod
    def find_by_user(user_id):
        tags_collection = mongo.db.tags
        return list(tags_collection.find({"user": ObjectId(user_id)}))

    @staticmethod
    def find_by_url(user_id, url_id):
        tags_collection = mongo.db.tags
        return list(tags_collection.find({
            "user": ObjectId(user_id),
            "urls": {"$in": [ObjectId(url_id)]}
        }))

    @staticmethod
    def delete_by_id(user_id, tag_id):
        tags_collection = mongo.db.tags
        result = tags_collection.delete_one(
            {"user": ObjectId(user_id), "_id": ObjectId(tag_id)})
        return result.deleted_count

    @staticmethod
    def update_by_id(tag_id, update_data):
        tags_collection = mongo.db.tags
        result = tags_collection.update_one(
            {"_id": ObjectId(tag_id)}, {"$set": update_data}
        )
        return result.modified_count

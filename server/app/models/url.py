from app import mongo
from bson.objectid import ObjectId


class Url:
    def __init__(self, user_id, original_url, short_url, shard_key, title=None, image=None, is_custom=False, tags=None, former_urls=None):
        self.user = user_id
        self.original_url = original_url
        self.short_url = short_url
        self.shard_key = shard_key
        self.title = title
        self.image = image
        self.is_custom = is_custom
        self.tags = tags if tags else []
        self.former_urls = former_urls if former_urls else []

    def save(self):
        urls_collection = mongo.db.urls
        urls_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_short_url(short_url):
        urls_collection = mongo.db.urls
        return urls_collection.find_one({"shortUrl": short_url})

    @staticmethod
    def find_by_id(userId, id):
        urls_collection = mongo.db.urls
        return urls_collection.find_one({"user": ObjectId(userId), "_id": ObjectId(id)})

    @staticmethod
    def find_by_user_id(user_id):
        urls_collection = mongo.db.urls
        return list(urls_collection.find({"user": ObjectId(user_id)}))

    @staticmethod
    def shorten_url(user_id, original_url, short_url, shard_key, title=None, image=None, is_custom=False, tags=None, former_urls=None):
        url_instance = Url(user_id, original_url, short_url,
                           shard_key, title, image, is_custom, tags, former_urls)
        url_instance.save()
        return url_instance.__dict__

    @staticmethod
    def delete_url(user_id, url_id):
        urls_collection = mongo.db.urls
        deleted_url = urls_collection.find_one_and_delete(
            {"_id": ObjectId(url_id), "user": ObjectId(user_id)})
        if deleted_url:
            return deleted_url
        else:
            return None

    @staticmethod
    def update_url(user_id, url_id, update_data):
        urls_collection = mongo.db.urls
        updated_url = urls_collection.find_one_and_update(
            {"_id": ObjectId(url_id), "user": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        return updated_url

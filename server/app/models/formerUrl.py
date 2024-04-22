from app import mongo
from bson.objectid import ObjectId


class FormerUrl:
    def __init__(self, user_id, original_url, short_url, shard_key, title=None, image=None, is_custom=False, tags=None, former_urls=None):
        self.user = user_id
        self.original_url = original_url
        self.short_url = short_url
        self.shard_key = shard_key
        self.title = title
        self.image = image
        self.is_custom = is_custom
        self.tags = tags if tags else []

    def save(self):
        urls_collection = mongo.db.formerurls
        urls_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_short_url(short_url):
        urls_collection = mongo.db.formerurls
        return urls_collection.find_one({"shortUrl": short_url})

    @staticmethod
    def find_by_id(user_id, id):
        urls_collection = mongo.db.formerurls
        return urls_collection.find_one({"user": ObjectId(user_id), "_id": ObjectId(id)})

    @staticmethod
    def find_by_user_id(user_id):
        urls_collection = mongo.db.formerurls
        return list(urls_collection.find({"user": ObjectId(user_id)}))

    @staticmethod
    def shorten_url(user_id, original_url, short_url, shard_key, title=None, image=None, is_custom=False, tags=None):
        url_instance = FormerUrl(
            user_id, original_url, short_url, shard_key, title, image, is_custom, tags)
        url_instance.save()
        return url_instance.__dict__

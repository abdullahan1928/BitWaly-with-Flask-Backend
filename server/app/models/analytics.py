from app import mongo
from datetime import datetime, timedelta
from bson.objectid import ObjectId


class Analytics():
    def __init__(self, url, ip_address, referrer, user_agent, device, browser, operating_system, vendor, location, utm_source, utm_medium, utm_campaign, utm_term, utm_content):
        self.url = url
        self.ip_address = ip_address
        self.referrer = referrer
        self.user_agent = user_agent
        self.device = device
        self.browser = browser
        self.operating_system = operating_system
        self.vendor = vendor
        self.location = location
        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign
        self.utm_term = utm_term
        self.utm_content = utm_content

    def save(self):
        self.save()

    @staticmethod
    def find_by_url(url):
        return list(mongo.db.analytics.find({"url": ObjectId(url)}))

    @staticmethod
    def find_by_id(id):
        return mongo.db.analytics.find_one({"_id": ObjectId(id)})

    @staticmethod
    def find_by_user_id(user_id):
        return list(mongo.db.analytics.find({"user": ObjectId(user_id)}))

    @staticmethod
    def find_by_url_id(url_id):
        return list(mongo.db.analytics.find({"url": ObjectId(url_id)}))

    @staticmethod
    def find_access_count(url_id):
        return mongo.db.analytics.count_documents({"url": ObjectId(url_id)})

    @staticmethod
    def find_weekly_count(url, start_date):
        return mongo.db.analytics.count_documents({
            "url": ObjectId(url),
            "accessedAt": {"$gte": start_date}
        })

    @staticmethod
    def find_weekly_change(url, start_date):
        total_clicks_last_7_days = mongo.db.analytics.count_documents({
            "url": ObjectId(url),
            "accessedAt": {"$gte": start_date}
        })

        total_clicks_last_14_days = mongo.db.analytics.count_documents({
            "url": ObjectId(url),
            "accessedAt": {"$gte": start_date - timedelta(days=7)}
        })

        if total_clicks_last_14_days == 0:
            return 100

        percentage_change = (
            (total_clicks_last_7_days - total_clicks_last_14_days) / total_clicks_last_14_days) * 100

        return percentage_change

    @staticmethod
    def clicks_data(url_id):
        click_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(url_id)}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$accessedAt"}},
                    "count": {"$sum": 1},
                },
            },
            {"$sort": {"_id": 1}},
        ])

        formatted_data = [{"date": data["_id"], "clicks": data["count"]}
                          for data in click_data]

        return formatted_data

    @staticmethod
    def click_data_per_url(url_id):
        click_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(url_id)}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$accessedAt"}},
                    "count": {"$sum": 1},
                },
            },
            {"$sort": {"_id": 1}},
        ])

        formatted_data = [{"date": data["_id"], "clicks": data["count"]}
                          for data in click_data]

        return formatted_data

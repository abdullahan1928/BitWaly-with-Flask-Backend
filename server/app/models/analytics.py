from app import db
from datetime import datetime


class Analytics(db.Document):
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
        return Analytics.objects(url=url)
    
    @staticmethod
    def find_by_id(id):
        return Analytics.objects(id=id)
    
    @staticmethod
    def find_by_user_id(user_id):
        return Analytics.objects(user_id=user_id)
    
    @staticmethod
    def find_by_url_id(url_id):
        return Analytics.objects(url=url_id)

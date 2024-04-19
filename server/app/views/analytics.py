from flask import Blueprint, request, jsonify
from app import mongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import json

analytics_blueprint = Blueprint('analytics', __name__, url_prefix='/analytics')

# Controller to fetch all analytics data for a specific URL


@analytics_blueprint.route('/all/<id>', methods=['GET'])
def all_analytics_controller(id):
    try:
        url_document = mongo.db.urls.find_one({"_id": ObjectId(id)})

        if not url_document:
            return jsonify({"error": "URL not found"}), 404

        analytics_data = mongo.db.analytics.find(
            {"url": ObjectId(id)}).sort("accessedAt", 1)

        formatted_data = []
        for data in analytics_data:
            formatted_data.append({
                "date": data["accessedAt"],
                "ipAddress": data["ipAddress"],
                "referrer": data["referrer"],
                "userAgent": data["userAgent"],
                "device": data["device"],
                "browser": data["browser"],
                "operatingSystem": data["operatingSystem"],
                "location": data["location"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching date analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch weekly click count for a URL


@analytics_blueprint.route('/weeklycount/<id>', methods=['GET'])
def weekly_count_controller(id):
    try:
        start_date = datetime.utcnow() - timedelta(days=7)

        click_data = mongo.db.analytics.count_documents({
            "url": ObjectId(id),
            "accessedAt": {"$gte": start_date}
        })

        return json.dumps(click_data, default=str), 200

    except Exception as e:
        print('Error in fetching click data:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch percentage change in weekly click count for a URL


@analytics_blueprint.route('/weeklychange/<id>', methods=['GET'])
def weekly_change_controller(id):
    try:
        start_date = datetime.utcnow() - timedelta(days=7)

        total_clicks_last_7_days = mongo.db.analytics.count_documents({
            "url": ObjectId(id),
            "accessedAt": {"$gte": start_date}
        })

        print('Total clicks last 7 days:', total_clicks_last_7_days)

        total_clicks_previous_week = mongo.db.analytics.count_documents({
            "url": ObjectId(id),
            "accessedAt": {"$lt": start_date, "$gte": start_date - timedelta(days=7)}
        })

        print('Total clicks previous week:', total_clicks_previous_week)

        percentage_change = ((total_clicks_last_7_days - total_clicks_previous_week) /
                             total_clicks_previous_week) * 100 if total_clicks_previous_week != 0 else 100

        print('Percentage change:', percentage_change)

        return json.dumps(percentage_change, default=str), 200

    except Exception as e:
        print('Error in fetching click data:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch access count for a URL


@analytics_blueprint.route('/accesscount/<id>', methods=['GET'])
def access_count_controller(id):
    try:
        access_data = mongo.db.analytics.count_documents({"url": ObjectId(id)})
        
        return json.dumps(access_data, default=str), 200

    except Exception as e:
        print('Error in fetching access data:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch browser analytics for a URL
@analytics_blueprint.route('/browser/<id>', methods=['GET'])
def browser_analytics_controller(id):
    try:
        browser_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id)}},
            {"$group": {"_id": "$browser", "count": {"$sum": 1}}}
        ])

        formatted_data = []
        for data in browser_data:
            formatted_data.append({
                "browser": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching browser analytics:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch OS analytics for a URL
@analytics_blueprint.route('/os/<id>', methods=['GET'])
def os_analytics_controller(id):
    try:
        os_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id)}},
            {"$group": {"_id": "$operatingSystem", "count": {"$sum": 1}}}
        ])

        formatted_data = []
        for data in os_data:
            formatted_data.append({
                "operatingSystem": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching OS analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch device analytics for a URL


@analytics_blueprint.route('/device/<id>', methods=['GET'])
def device_analytics_controller(id):
    try:
        device_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id)}},
            {"$group": {"_id": "$device", "count": {"$sum": 1}}}
        ])

        formatted_data = []
        for data in device_data:
            formatted_data.append({
                "device": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching device analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch mobile vendor analytics for a URL


@analytics_blueprint.route('/mobile/<id>', methods=['GET'])
def vendor_analytics_controller(id):
    try:
        vendor_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id), "device": "mobile"}},
            {"$group": {"_id": "$vendor", "count": {"$sum": 1}}
             }
        ])

        formatted_data = []
        for data in vendor_data:
            formatted_data.append({
                "vendor": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching vendor analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch location analytics for a URL


@analytics_blueprint.route('/location/<id>', methods=['GET'])
def location_analytics_controller(id):
    try:
        location_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id)}},
            {"$group": {"_id": "$location", "count": {"$sum": 1}}
             }
        ])

        formatted_data = []
        for data in location_data:
            formatted_data.append({
                "location": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching location analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch referrer analytics for a URL


@analytics_blueprint.route('/referrer/<id>', methods=['GET'])
def referrer_analytics_controller(id):
    try:
        referrer_data = mongo.db.analytics.aggregate([
            {"$match": {"url": ObjectId(id)}},
            {"$group": {"_id": "$referrer", "count": {"$sum": 1}}
             }
        ])

        formatted_data = []
        for data in referrer_data:
            formatted_data.append({
                "referrer": data["_id"],
                "count": data["count"]
            })

        return json.dumps(formatted_data, default=str), 200

    except Exception as e:
        print('Error in fetching referrer analytics:', e)
        return jsonify({"error": "Server error"}), 500

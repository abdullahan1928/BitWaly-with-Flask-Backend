from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from app.models.url import Url
from app.models.formerUrl import FormerUrl
from app.models.analytics import Analytics
from app.middlewares.fetch_user import fetch_user

analytics_blueprint = Blueprint('analytics', __name__, url_prefix='/analytics')

# Controller to fetch access count for a URL


@analytics_blueprint.route('/accesscount/<id>', methods=['GET'])
@fetch_user
def access_count_controller(id):
    try:
        access_data = Analytics.find_access_count(id)

        return json.dumps(access_data, default=str), 200

    except Exception as e:
        print('Error in fetching access data:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch weekly click count for a URL

@analytics_blueprint.route('/weeklycount/<id>', methods=['GET'])
@fetch_user
def weekly_count_controller(id):
    try:
        start_date = datetime.utcnow() - timedelta(days=7)

        click_data = Analytics.find_weekly_count(id, start_date)

        return json.dumps(click_data, default=str), 200

    except Exception as e:
        print('Error in fetching click data:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch percentage change in weekly click count for a URL


@analytics_blueprint.route('/weeklychange/<id>', methods=['GET'])
@fetch_user
def weekly_change_controller(id):
    try:
        start_date = datetime.utcnow() - timedelta(days=7)

        percentage_change = Analytics.find_weekly_change(id, start_date)

        return json.dumps(percentage_change, default=str), 200

    except Exception as e:
        print('Error in fetching click data:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch click data (date-wise) for a URL
@analytics_blueprint.route('/clicks/<id>', methods=['GET'])
@fetch_user
def click_data_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        clicks = Analytics.clicks_data(url["_id"])

        return json.dumps(clicks, default=str), 200

    except Exception as e:
        print('Error in fetching click data:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch browser analytics for a URL
@analytics_blueprint.route('/browser/<id>', methods=['GET'])
@fetch_user
def browser_analytics_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        browsers = []
        for data in analytics_data:
            browsers.append({
                "browser": data["browser"],
                "date": data["accessedAt"]
            })

        return json.dumps(browsers, default=str), 200

    except Exception as e:
        print('Error in fetching browser analytics:', e)
        return jsonify({"error": "Server error"}), 500


# Controller to fetch OS analytics for a URL
@analytics_blueprint.route('/os/<id>', methods=['GET'])
@fetch_user
def os_analytics_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        os = []
        for data in analytics_data:
            os.append({
                "os": data["operatingSystem"],
                "date": data["accessedAt"]
            })

        return json.dumps(os, default=str), 200

    except Exception as e:
        print('Error in fetching OS analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch device analytics for a URL


@analytics_blueprint.route('/device/<id>', methods=['GET'])
@fetch_user
def device_analytics_controller(id):

    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        devices = []
        for data in analytics_data:
            devices.append({
                "device": data["device"],
                "date": data["accessedAt"]
            })

        return json.dumps(devices, default=str), 200

    except Exception as e:
        print('Error in fetching device analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch mobile vendor analytics for a URL


@analytics_blueprint.route('/mobile/<id>', methods=['GET'])
@fetch_user
def vendor_analytics_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        vendors = []
        for data in analytics_data:
            vendors.append({
                "vendor": data["vendor"],
                "date": data["accessedAt"]
            })

        return json.dumps(vendors, default=str), 200

    except Exception as e:
        print('Error in fetching vendor analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch location analytics for a URL


@analytics_blueprint.route('/location/<id>', methods=['GET'])
@fetch_user
def location_analytics_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        locations = []
        for data in analytics_data:
            locations.append({
                "date": data["accessedAt"],
                "country": data["location"]["country"],
                "city": data["location"]["city"],
            })

        return json.dumps(locations, default=str), 200

    except Exception as e:
        print('Error in fetching location analytics:', e)
        return jsonify({"error": "Server error"}), 500

# Controller to fetch referrer analytics for a URL


@analytics_blueprint.route('/referrer/<id>', methods=['GET'])
@fetch_user
def referrer_analytics_controller(id):
    try:
        user_id = request.user_id
        url = Url.find_by_id(user_id, id) or FormerUrl.find_by_id(user_id, id)

        analytics_data = Analytics.find_by_url_id(url["_id"])

        referrers = []
        for data in analytics_data:
            referrers.append({
                "referrer": data["referrer"],
                "date": data["accessedAt"]
            })

        return json.dumps(referrers, default=str), 200

    except Exception as e:
        print('Error in fetching referrer analytics:', e)
        return jsonify({"error": "Server error"}), 500

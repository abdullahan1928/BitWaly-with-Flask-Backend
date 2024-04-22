from flask import Blueprint, jsonify, request, current_app
from app.models.url import Url
from app.models.analytics import Analytics
from bson.objectid import ObjectId
from app.middlewares.fetch_user import fetch_user
import json

summary_blueprint = Blueprint('summary', __name__, url_prefix='/summary')

# Controller to get total clicks for all URLs of a user


@summary_blueprint.route('/clicks')
@fetch_user
def total_clicks():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        total_clicks = sum(url["accessCount"] for url in user_urls)
        first_link_date = user_urls[0]["createdAt"] if user_urls else None

        return json.dumps({'totalClicks': total_clicks, 'firstLinkDate': first_link_date}, default=str), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

# Controller to get device-wise clicks for all URLs of a user


@summary_blueprint.route('/devices')
@fetch_user
def device_clicks():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        all_analytics = [
            analytics for url in user_urls
            for analytics in Analytics.find_by_url_id(url["_id"])
        ]

        device_counts = {}
        for analytics in all_analytics:
            device_type = analytics["device"] or 'Unknown'
            device_counts[device_type] = device_counts.get(device_type, 0) + 1

        device_data = [{'device': device, 'count': count}
                       for device, count in device_counts.items()]

        return json.dumps(device_data), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

# Controller to get referrer-wise clicks for all URLs of a user


@summary_blueprint.route('/referrers')
@fetch_user
def referrer_clicks():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        all_analytics = [
            analytics for url in user_urls
            for analytics in Analytics.find_by_url_id(url["_id"])
        ]

        referrer_counts = {}
        for analytics in all_analytics:
            referrer = analytics["referrer"] or 'Direct'
            referrer_counts[referrer] = referrer_counts.get(referrer, 0) + 1

        referrer_data = [{'referrer': referrer, 'count': count}
                         for referrer, count in referrer_counts.items()]

        return json.dumps(referrer_data), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

# Controller to get all locations (countries and cities) for all URLs of a user


@summary_blueprint.route('/locations')
@fetch_user
def all_locations():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        all_analytics = [
            analytics for url in user_urls
            for analytics in Analytics.find_by_url_id(url["_id"])
        ]

        location_counts = {'countries': {}, 'cities': {}}

        for analytics in all_analytics:
            country, city = analytics["location"]["country"], analytics["location"]["city"]
            location_counts['countries'][country] = location_counts['countries'].get(
                country, 0) + 1
            location_counts['cities'][city] = location_counts['cities'].get(
                city, 0) + 1

        location_data = {
            'countries': [{'country': country, 'count': count} for country, count in location_counts['countries'].items()],
            'cities': [{'city': city, 'count': count} for city, count in location_counts['cities'].items()]
        }

        return json.dumps(location_data), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

# Controller to get top locations (cities) for all URLs of a user


@summary_blueprint.route('/toplocations')
@fetch_user
def top_locations():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        all_analytics = [
            analytics for url in user_urls
            for analytics in Analytics.find_by_url_id(url["_id"])
        ]

        location_counts = {'cities': {}}
        for analytics in all_analytics:
            city = analytics["location"]["city"]
            location_counts['cities'][city] = location_counts['cities'].get(
                city, 0) + 1

        sorted_cities = sorted(
            location_counts['cities'].items(), key=lambda x: x[1], reverse=True)[:3]

        location_data = [{'city': city, 'count': count}
                         for city, count in sorted_cities]

        return jsonify(location_data), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

# Controller to get clicks with dates for all URLs of a user


@summary_blueprint.route('/clickswithdates')
@fetch_user
def clicks_with_dates():
    try:
        user_id = request.user_id

        user_urls = Url.find_by_user_id(user_id)

        click_data = []
        for url in user_urls:
            click_data_per_url = Analytics.click_data_per_url(url["_id"])

            click_data.extend(click_data_per_url)

        merged_data = {}
        for data in click_data:
            date = data['date']
            clicks = data['clicks']
            merged_data[date] = merged_data.get(date, 0) + clicks

        merged_data_list = [{'date': date, 'clicks': clicks}
                            for date, clicks in merged_data.items()]

        return jsonify(merged_data_list), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error='Server error'), 500

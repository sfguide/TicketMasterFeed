import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
TICKETMASTER_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

@app.route("/")
def index():
    return "Ticketmaster proxy is running."

@app.route("/events")
def get_events():
    if not TICKETMASTER_API_KEY:
        return jsonify({"error": "Missing TICKETMASTER_API_KEY"}), 500

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "size": 50,
        "countryCode": "US",
        "city": os.getenv("EVENT_CITY", "Sarasota"),
        "sort": "date,asc"
    }
    # Example filtering parameters
    start = request.args.get("start")  # e.g. "2025-08-01T00:00:00Z"
    end   = request.args.get("end")    # e.g. "2025-08-31T23:59:59Z"
    className = request.args.get("classificationName")  # e.g. "music"

    if start:
        params["startDateTime"] = start
    if end:
        params["endDateTime"] = end
    if className:
        params["classificationName"] = className

    response = requests.get(TICKETMASTER_BASE_URL, params=params)
    if response.ok:
        return jsonify(response.json())
    return jsonify({"error": response.text}), response.status_code

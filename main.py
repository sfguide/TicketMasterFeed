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
        "size": 10,
        "countryCode": "US",
        "city": "Sarasota",
        "sort": "date,asc"
    }

    try:
        response = requests.get(TICKETMASTER_BASE_URL, params=params)
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

@app.route("/")
def home():
    return "Ticketmaster proxy is running."

@app.route("/events")
def events():
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "size": 30,
        "sort": "date,asc"
    }

    # Optional filters
    city = request.args.get("city")
    start = request.args.get("startDateTime")
    end = request.args.get("endDateTime")
    classification = request.args.get("classificationName")

    if city:
        params["city"] = city
    if start:
        params["startDateTime"] = start
    if end:
        params["endDateTime"] = end
    if classification:
        params["classificationName"] = classification

    print("➡️ Ticketmaster API Request Params:", params)

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

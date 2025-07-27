from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests

app = Flask(__name__)
CORS(app)

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE = "https://app.ticketmaster.com/discovery/v2/events.json"

@app.route("/events")
def get_events():
    if not TICKETMASTER_API_KEY:
        return jsonify({"error": "Missing TICKETMASTER_API_KEY"}), 500

    params = {"apikey": TICKETMASTER_API_KEY, "size": 20, "countryCode": "US"}

    city = request.args.get("city")
    if city:
        params["city"] = city

    start = request.args.get("start")
    if start:
        params["startDateTime"] = start

    end = request.args.get("end")
    if end:
        params["endDateTime"] = end

    className = request.args.get("classificationName")
    if className:
        params["classificationName"] = className

    resp = requests.get(BASE, params=params)
    return jsonify(resp.json()) if resp.ok else jsonify({"error": resp.text}), resp.status_code

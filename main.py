from flask import Flask, jsonify, request
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
    for p in ("start", "end", "classificationName", "city"):
        v = request.args.get(p)
        if v:
            # Ticketmaster expects ISO8601 with Z
            key = {"start": "startDateTime", "end": "endDateTime"}.get(p, p)
            params[key] = v

    resp = requests.get(BASE, params=params)
    return jsonify(resp.json()) if resp.ok else jsonify({"error": resp.text}), resp.status_code

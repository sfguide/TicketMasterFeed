from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Use environment variable or hardcode your TM API key
TM_API_KEY = os.environ.get("TICKETMASTER_API_KEY") or "YOUR_TICKETMASTER_API_KEY"

@app.route("/")
def home():
    return "Ticketmaster proxy is running."

@app.route("/events")
def get_events():
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
        "apikey": TM_API_KEY,
        "city": request.args.get("city"),
        "classificationName": request.args.get("classificationName"),
        "startDateTime": request.args.get("start"),
        "endDateTime": request.args.get("end"),
        "sort": request.args.get("sort")
    }

    # Remove any None values so they don't mess up the request
    filtered_params = {k: v for k, v in params.items() if v}

    try:
        response = requests.get(base_url, params=filtered_params)
        data = response.json()
        print("Proxy forwarded params:", filtered_params)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

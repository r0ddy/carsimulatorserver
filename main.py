from flask import Flask, request
import json
import os
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
devices = []
not_authorized = json.dumps({"error": "need password"})

@app.route("/devices", methods=['POST'])
def hello_world():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    return json.dumps({"devices": devices})

@app.route('/register', methods=['POST'])
def update_text():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    else:
        device = {"ip": data["ip"], "type": data["type"]}
        devices.append(device)
        return json.dumps({"msg": "ok"})
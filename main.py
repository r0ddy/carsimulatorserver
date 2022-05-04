from flask import Flask, request
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
devices = {}
not_authorized = json.dumps({"error": "need password"})

def send_data(url, data):
    data['password'] = PASSWORD
    res = requests.post(url, json=data)
    return res

@app.route("/devices", methods=['POST'])
def get_devices():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    return json.dumps({"devices": devices})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    else:
        global devices
        device = {"ip": data["ip"]}
        devices[data['type']] = device
        return json.dumps({"msg": "ok"})

@app.route('/notify_bot', methods=['POST'])
def notify_bot():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    elif "bot" in devices:
        ip = devices["bot"]["ip"]
        res = send_data(ip, data['state'])
        json.dumps({'msg': 'msg received; bot responded with ' + res.status_code})
    else:
        print(data["action"])
        json.dumps({'msg': 'msg received; no bot to notify'})

@app.route('/rest', methods=['POST'])
def reset():
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    else:
        global devices
        devices = {}
        return json.dumps({'msg': 'server reset'})
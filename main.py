from flask import Flask, request
import json
import os
from dotenv import load_dotenv
import requests
from flask_socketio import SocketIO, ConnectionRefusedError

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
socketio = SocketIO(app)

devices = {}
not_authorized = json.dumps({"error": "need password"})

def send_data(url, data):
    data['password'] = PASSWORD
    res = requests.post(url, json=data)
    return res

@app.route("/devices", methods=['POST'])
def get_devices():
    global devices
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    return json.dumps({"devices": devices})

@app.route('/register', methods=['POST'])
def register():
    global devices
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    else:
        device = {"ip": data["ip"]}
        devices[data['type']] = device
        return json.dumps({"devices": devices})

@app.route('/notify_bot', methods=['POST'])
def notify_bot():
    global devices
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    elif "bot" in devices:
        ip = devices["bot"]["ip"]
        res = send_data(ip, data['state'])
        return json.dumps({'msg': 'msg received; bot responded with ' + res.status_code})
    else:
        print(data["action"])
        return json.dumps({'msg': 'msg received; no bot to notify'})

@app.route('/reset', methods=['POST'])
def reset():
    global devices
    data = request.get_json()
    if data['password'] != PASSWORD:
        return not_authorized
    else:
        devices = {}
        return json.dumps({'msg': 'server reset'})

@socketio.on('connect')
def connect():
    if request.headers['password'] != PASSWORD:
        raise ConnectionRefusedError('need password')

@socketio.on('')

if __name__ == '__main__':
    socketio.run(app)

# put controller into room
# put phone into room
# put pi bot into room
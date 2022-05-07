from flask import Flask, request
import json
import os
from dotenv import load_dotenv
import requests
from flask_socketio import SocketIO, ConnectionRefusedError, join_room, emit

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

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

class DeviceType:
    BOT = 'bot'
    PHONE = 'phone'
    CONTROLLER = 'controller'

@socketio.on('connect',namespace='/device_network')
def connect():
    if request.headers['password'] != PASSWORD:
        raise ConnectionRefusedError('need password')

@socketio.on('join',namespace='/device_network')
def on_join(data):
    print("new device joined")
    join_room(data['device_type'])
    emit('notif', {'msg': 'hello'}, namespace='/device_network')

@socketio.on('send_msg',namespace='/device_network')
def send_msg(data):
    # the bot only sends camera data so send this to the phone
    if data['device_type'] == DeviceType.BOT:
        print("send msg from bot to phone")
        emit('notif', data['msg'], namespace='/device_network', to=DeviceType.PHONE)
    # send angles to bot
    elif data['device_type'] == DeviceType.CONTROLLER:
        emit('notif', data['msg'], namespace='/device_network', to=DeviceType.BOT)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=3000, debug=True)

# put controller into room
# put phone into room
# put pi bot into room
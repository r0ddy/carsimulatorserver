import eventlet
import socketio
import logging
import os
from dotenv import load_dotenv

class DeviceType:
    BOT = 'bot'
    PHONE = 'phone'
    CONTROLLER = 'controller'


log = logging.getLogger('event-logger')
sio = socketio.Server()
app = socketio.WSGIApp(sio)
load_dotenv()
PASSWORD = os.getenv("PASSWORD")

@sio.event
def connect(sid, environ):
    print("connected")

@sio.on('join')
def join(sid, data):
    device_type = data['device_type']
    log.info("joining {} room".format(device_type))
    sio.enter_room(sid, device_type)

@sio.on('send_msg')
def send_msg(sid, data):
    device_type = data['device_type']
    # the bot only sends camera data so send this to the phone
    if device_type == DeviceType.BOT:
        log.info("send msg from bot to phone")
        sio.emit('notif', data['msg'], room=DeviceType.PHONE)
    # send angles to bot
    elif device_type == DeviceType.CONTROLLER:
        log.info('send msg from controller to bot')
        sio.emit('notif', data['msg'], room=DeviceType.BOT)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)),app)
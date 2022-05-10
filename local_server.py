import eventlet
import socketio
import socket

from devicetypes import DeviceType

client = socketio.Client()
client.connect('ws://car-simulator-349213.uk.r.appspot.com/')
name = socket.gethostname()
ip_addr = socket.gethostbyname_ex(name)[2][-1]
client.emit('join', {'device_type': DeviceType.COMPUTER, 'ip': ip_addr })

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': './static'})

@sio.on('join')
def join(sid, data):
    device_type = data['device_type']
    sio.enter_room(sid, device_type)

@sio.on('send_msg')
def send_msg(sid, data):
    device_type = data['device_type']
    # the bot only sends camera data so send this to the phone
    if device_type == DeviceType.BOT:
        sio.emit('notif', data['msg'], room=DeviceType.PHONE)
    # send angles to bot
    elif device_type == DeviceType.CONTROLLER:
        sio.emit('notif', data['msg'], room=DeviceType.BOT)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)),app)
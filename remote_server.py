import eventlet
import socketio
from devicetypes import DeviceType

sio = socketio.Server()
app = socketio.WSGIApp(sio)

NON_COMPUTER_ROOM = "non_computer_room"
LOCAL_SERVER_IP = None
@sio.on('join')
def join(sid, data):
    global LOCAL_SERVER_IP
    device_type = data['device_type']
    if device_type != DeviceType.COMPUTER:
        sio.enter_room(sid, NON_COMPUTER_ROOM)
    else:
        LOCAL_SERVER_IP = data['ip']
    if LOCAL_SERVER_IP:
        sio.emit('server_on', {'ip': LOCAL_SERVER_IP}, room=NON_COMPUTER_ROOM)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)),app)
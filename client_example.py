import socketio
sio = socketio.Client()

@sio.on('notif')
def on_message(data):
    print(data)

sio.connect('https://devicenetwork-dot-car-simulator-349213.uk.r.appspot.com/')
sio.emit('join', {'device_type': 'phone'})
sio.wait()

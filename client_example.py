import socketio
sio = socketio.Client()

sio.connect('http://127.0.0.1:5000', headers={'password': 'ithaca123'})

sio.emit('msg', {'data': 'foo'})

sio.disconnect()
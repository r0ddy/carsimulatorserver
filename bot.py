import socketio
sio = socketio.Client()
@sio.on('notif')
def on_message(data):
    print('I received a message!')

sio.connect('https://devicenetwork-dot-car-simulator-349213.uk.r.appspot.com/')
sio.emit('join', {'device_type': 'bot'})

def send_data(arg):
    res = ""
    while res != "exit":
        res = input("Enter a message: ")
        sio.emit("send_msg", {"msg": res, "device_type": "bot"})
sio.start_background_task(send_data, 123)

sio.wait()

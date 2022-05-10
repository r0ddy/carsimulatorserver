import socketio
client = socketio.Client()
client.connect('ws://car-simulator-349213.uk.r.appspot.com/')
client.emit('join', {'device_type': 'bot'})
LOCAL_SERVER_URL = None

@client.on('notif')
def on_message(data):
    print(data)

# wait for local server to turn on and send its ip
@client.on('server_on')
def server_on(data):
    global LOCAL_SERVER_URL
    LOCAL_SERVER_URL = "ws://{}:3000/".format(data["ip"])
    client.disconnect()

# wait until local server url received
client.wait()
client.connect(LOCAL_SERVER_URL)
client.emit('join', {'device_type': 'bot'})

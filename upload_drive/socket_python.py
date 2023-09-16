import socketio
import eventlet

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

# Create a Socket.IO application
app = socketio.WSGIApp(sio)

# Define an event handler for the 'connect' event
@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

# Define an event handler for the 'message' event
@sio.event
def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Broadcast the message to all connected clients
    sio.emit('message', data)

# Define an event handler for the 'disconnect' event
@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)

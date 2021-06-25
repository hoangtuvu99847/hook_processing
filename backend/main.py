# RUN HERE
import socketio
from tools.collection_tool import CollectionTool
import socket

hostname = socket.gethostname()

sio = socketio.Client()


@sio.event
def connect():
    print('connected to server')
    collect()


@sio.event
def disconnect():
    print('disconnected from server')


def collect():
    while True:
        result = CollectionTool().run()
        result.update({
            'client': hostname
        })
        print(result)
        sio.emit('manager', result)


if __name__ == '__main__':
    sio.connect('http://localhost:9999', headers={'client_id': hostname},
                auth={'token': 'my-token'})
    sio.wait()

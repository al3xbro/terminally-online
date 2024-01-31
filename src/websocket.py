import json
from websockets.sync.client import connect
from websockets.client import ClientConnection
import time
import threading

# get login token TODO: move to auth.py and change token storage
f = open('token.json', 'r')
token = json.load(f).get('token')
f.close()

def __connect_websocket() ->  ClientConnection:
    """Connects to Discord websocket with user token. Do not invoke."""

    # websocket handshake
    ws = connect('wss://gateway.discord.gg/?v=9&encoding=json', max_size=999999999)
    # get hello and heartbeat interval
    reply = json.loads(ws.recv())

    # start heartbeat thread
    interval = reply['d']['heartbeat_interval']
    threading.Thread(target = heartbeat, args = (interval, ws)).start()

    # identify yourself
    ws.send(json.dumps({
        'op': 2,
        'd': {
            'token': token,
            'compress': False,
            'properties': {
                '$os': 'Windows',
                '$browser': 'Chrome',
                '$device': ''
            }
        }
    }))

    return ws

def heartbeat(interval, ws):
    """Heartbeat for websocket connection"""

    # TODO: send accurate d value
    print("heartbeat")
    while True:
        time.sleep(interval / 1000)
        ws.send(json.dumps({
            'op': 1,
            'd': None
        }))
        
def get_websocket():
    """Returns ClientConnection object"""

    global ws
    return ws

ws = __connect_websocket()
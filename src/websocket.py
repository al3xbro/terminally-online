import json
from websockets.sync.client import connect
from websockets.client import ClientConnection
import time
import threading

class Connection:
    def __init__(self):

        # get login token TODO: move to auth.py and change token storage
        f = open('token.json', 'r')
        self.token = json.load(f).get('token')
        f.close()

        if self.ws == None:
            self.__connect_websocket()

    def __connect_websocket(self) ->  ClientConnection:
        """Connects to Discord websocket with user token. Do not invoke."""

        # websocket handshake
        ws = connect('wss://gateway.discord.gg/?v=9&encoding=json', max_size=999999999)
        # get hello and heartbeat interval
        reply = json.loads(ws.recv())

        # start heartbeat thread
        interval = reply['d']['heartbeat_interval']
        threading.Thread(target = self.heartbeat, args = (interval, ws)).start()

        # identify yourself
        ws.send(json.dumps({
            'op': 2,
            'd': {
                'token': self.token,
                'compress': False,
                'properties': {
                    '$os': 'Windows',
                    '$browser': 'Chrome',
                    '$device': ''
                }
            }
        }))

        self.ws = ws
        return self.ws

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
            
    def get_websocket(self):
        """Returns ClientConnection object"""

        return self.ws
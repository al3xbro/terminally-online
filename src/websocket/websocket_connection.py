import json
import time
import threading
from auth import auth

from websockets.sync.client import connect
from websockets.client import ClientConnection

class Connection:

    # static ws object
    ws = None

    @staticmethod
    def __connect_websocket() ->  ClientConnection:
        '''Connects to Discord websocket with user token. Do not invoke.'''

        # websocket handshake
        ws = connect('wss://gateway.discord.gg/?v=9&encoding=json', max_size=999999999)
        # get hello and heartbeat interval
        reply = json.loads(ws.recv())

        # start heartbeat thread
        interval = reply['d']['heartbeat_interval']
        threading.Thread(target = Connection.__heartbeat, args = (interval, ws)).start()

        # identify yourself
        ws.send(json.dumps({
            'op': 2,
            'd': {
                'token': auth.get_token(),
                'compress': False,
                'properties': {
                    '$os': 'Windows',
                    '$browser': 'Chrome',
                    '$device': ''
                }
            }
        }))

        return ws

    @staticmethod
    def __heartbeat(interval, ws):
        '''Heartbeat for websocket connection. Do not invoke'''

        # TODO: send accurate d value
        while True:
            time.sleep(interval / 1000)
            ws.send(json.dumps({
                'op': 1,
                'd': None
            }))
            
    @staticmethod
    def get_websocket() -> ClientConnection:
        '''Returns ClientConnection object'''
        
        if Connection.ws:
            return Connection.ws
        else:
            Connection.ws = Connection.__connect_websocket()
            return Connection.ws
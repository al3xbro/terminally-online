import json
import time
import threading
import requests
from auth import auth

from websockets.sync.client import connect
from websockets import ConnectionClosed
from websockets.client import ClientConnection

class Connection:

    ws = None
    gateway_url = None
    heartbeat_thread = None
    heartbeat_interval = None

    @staticmethod
    def get_websocket() -> ClientConnection:
        '''Returns ClientConnection object.'''
        
        # connect if not connected
        if not Connection.ws:
            Connection.__connect_websocket()

        return Connection.ws
        

    @staticmethod
    def reconnect_websocket(reconnect_url: str, session_id: str = '') -> None:
        '''Reconnects to Discord websocket.'''

        # websocket handshake
        ws = connect(f'{reconnect_url}/?v=9&encoding=json', max_size=999999999)
        # send resume event
        ws.send(json.dumps({
            'op': 6,
            'd': {
                'token': auth.get_token(),
                'session_id': session_id,
                'seq': 0
            }
        }))
        # update ws object
        Connection.ws = ws
        # start new heartbeat thread
        Connection.heartbeat_thread = threading.Thread(target = Connection.__heartbeat, args = (Connection.heartbeat_interval, Connection.ws))

    @staticmethod
    def __connect_websocket() ->  ClientConnection:
        '''Connects to Discord websocket with user token.'''

        # get gateway url
        Connection.gateway_url = requests.get('https://discord.com/api/v9/gateway').json().get('url')

        # websocket handshake
        ws = connect(f'{Connection.gateway_url}/?v=9&encoding=json', max_size=999999999)
        # get hello and heartbeat interval
        reply = json.loads(ws.recv())

        # start heartbeat thread
        Connection.heartbeat_interval = reply['d']['heartbeat_interval']
        Connection.heartbeat_thread = threading.Thread(target = Connection.__heartbeat, args = (Connection.heartbeat_interval, ws))
        Connection.heartbeat_thread.start()

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

        Connection.ws = ws

    @staticmethod
    def __heartbeat(interval: int, ws: ClientConnection) -> None:
        '''Heartbeat for websocket connection.'''

        # TODO: send accurate d value
        is_connected = True
        while is_connected:
            try:
                time.sleep(interval / 1000)
                ws.send(json.dumps({
                    'op': 1,
                    'd': None
                }))
            except ConnectionClosed:
                is_connected = False
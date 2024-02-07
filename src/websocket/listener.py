import json
from collections import defaultdict

from websockets import ConnectionClosed
from websocket.connection import Connection
import threading

class Listener:
    
    # { event_id: [callback] }
    events = defaultdict(lambda: list())
    reconnect_url = None
    session_id = None

    @staticmethod
    def subscribe_event(event_id: str, callback: callable) -> None:
        '''Invokes callback whenever receiving event_id. The callback function must take one argument.''' # TODO: figure out how to specify callable arguments

        if event_id not in Listener.events:
            Listener.events[event_id] = [callback]
        else:
            Listener.events[event_id].append(callback)

    @staticmethod
    def __listener_loop():
        '''Listens for events and invokes callbacks.'''

        # executes callbacks for each event, passing data
        while True:
            try: 
                reply = json.loads(Connection.get_websocket().recv())

                # on ready, update reconnect_url and session_id
                if reply.get('t') == 'READY':
                    Listener.reconnect_url = reply.get('d').get('resume_gateway_url')
                    Listener.session_id = reply.get('d').get('session_id')
                
                # if event has been registered, execute callbacks
                for callback in Listener.events[reply.get('t')]:
                    callback(reply.get('d'))

            # reconnect on connection closed
            except ConnectionClosed:
                try:
                    Connection.reconnect_websocket(Connection.reconnect_url, Connection.session_id)
                except:
                    Connection.reconnect_websocket(Connection.gateway_url)

    # start listener loop
    threading.Thread(target = __listener_loop).start()
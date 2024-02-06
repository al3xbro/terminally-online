import json
from collections import defaultdict
from websocket.connection import Connection
import threading

class Listener:
    
    # { event_id: [callback] }
    events = defaultdict(lambda: list())

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
            reply = json.loads(Connection.get_websocket().recv())
            
            # if event has been registered, execute callbacks
            for callback in Listener.events[reply.get('t')]:
                callback(reply.get('d'))

    # start listener loop
    threading.Thread(target = __listener_loop).start()
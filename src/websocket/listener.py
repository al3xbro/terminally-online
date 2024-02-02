import json
from collections import defaultdict
from websocket.connection import Connection
import threading

class Listener:
    
    # { event: [callback] }
    events = defaultdict(lambda: list())

    @staticmethod
    def add_event(event: str, callback: callable) -> None:
        '''Adds an event and its callback to event dictionary. The callback function must take one argument.''' # TODO: figure out how to specify callable arguments

        if event not in Listener.events:
            Listener.events[event] = [callback]
        else:
            Listener.events[event].append(callback)

    @staticmethod
    def __listener_loop():
        '''Listens for events and calls callbacks.'''

        # executes callbacks for each event, passing data
        while True:
            reply = json.loads(Connection.get_websocket().recv())
            
            # if event has been registered, execute callbacks
            for callback in Listener.events[reply.get('t')]:
                callback(reply.get('d'))

    threading.Thread(target = __listener_loop).start()
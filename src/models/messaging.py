from queue import Queue
import requests
import json
from utils.mlist import MessageList

from auth import auth
from websocket.listener import Listener

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

class Messaging:
    
    # { 
    #     channel_id: MessageList
    # }
    __subscribed_channels = {}
    queue = Queue()

    @staticmethod
    def subscribe_channel(channel_id: str) -> None:
        '''Add a channel to a list of subscribed channels. The callback function is invoked when a new message is received.'''

        # check if already subscribed
        if channel_id in Messaging.__subscribed_channels:
            return

        # add channel to subscribed channels and populate cache TODO: come up with cache eviction policy
        history = Messaging.__get_message_history(channel_id)

        # add to cache
        Messaging.__subscribed_channels[channel_id] = (
            MessageList(history),
        )

    @staticmethod
    def get_messages(channel_id: str) -> list:
        '''Returns the list of messages in the current channel. The channel must be already subscribed to.'''

        return Messaging.__subscribed_channels[channel_id][0] # TODO: change based on cache eviction policy

    @staticmethod
    def request_older_messages(channel_id: str) -> None:
        '''Requests old messages from the server before message_id. The channel must be already subscribed to.'''

        # get oldest message in cache
        iterator = iter(Messaging.__subscribed_channels[channel_id][0])

        # get history
        history = Messaging.__get_message_history(channel_id, before=next(iterator).get('id'))[::-1]
        
        # tell the view to add messages
        Messaging.queue.put({
            'type': 'p',
            'data': history[::-1]
        })

        # add to cache
        for message in history:
            Messaging.__subscribed_channels[channel_id][0].prepend(message.get('id'), message)

    @staticmethod
    def send_message(channel_id: str, content: str):
        '''Sends a message to channel'''

        # send request
        res = requests.post(
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages', 
            headers = headers | { 'authorization': auth.get_token() },
            data = json.dumps({ 'content': content })
        )
        
        # return status TODO: better error handling and documentation
        if res.status_code == 200:
            return True
        return False
    
    @staticmethod
    def __get_message_history(channel_id: str, limit: int = 50, before: str = None) -> list:
        '''Returns a list of past messages in the current channel.'''

        # send request
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}&before={before}' if before else f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}'
        res = requests.get(
            url = url, 
            headers = headers | { 'authorization': auth.get_token() }
        )
        
        # return messages in reverse chronological order TODO: better error handling and documentation
        try:
            return list(res.json())[::-1]
        except:
            return []

    @staticmethod
    def __append_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # add message to cache
            channel_id[0].append(message_data.get('id'), message_data)
            # tell the view to add the message
            Messaging.queue.put({
                'type': 'a', 
                'data': message_data
            })
            
    @staticmethod
    def __delete_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # remove message from cache
            channel_id[0].delete(message_data.get('id'))
            # tell the view to remove the message
            Messaging.queue.put({
                'type': 'd', 
                'data': message_data
            })

    @staticmethod
    def __edit_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # edit message in cache
            channel_id[0].edit(message_data.get('id'), message_data)
            # tell the view to edit the message
            Messaging.queue.put({
                'type': 'e', 
                'data': message_data
            })

    Listener.subscribe_event('MESSAGE_CREATE', __append_message)
    Listener.subscribe_event('MESSAGE_DELETE', __delete_message)
    Listener.subscribe_event('MESSAGE_UPDATE', __edit_message)
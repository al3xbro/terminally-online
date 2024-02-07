import requests
import json
from collections import defaultdict

from auth import auth
from websocket.listener import Listener

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

class Messaging:
    
    # { channel_id: ([message_dict], {message_id: message_index}, callback) }
    __subscribed_channels = defaultdict(None)

    @staticmethod
    def subscribe_channel(channel_id: str, callback: callable) -> None:
        '''Add a channel to a list of subscribed channels. The callback function is invoked when a new message is recieved.'''

        # check if already subscribed
        if channel_id in Messaging.__subscribed_channels:
            return

        # add channel to subscribed channels and populate cache TODO: come up with cache eviction policy
        history = Messaging.__get_message_history(channel_id)

        Messaging.__subscribed_channels[channel_id] = (
            history, 
            { message.get('id'): i for i, message in enumerate(history) },
            callback
        )

    @staticmethod
    def get_messages(channel_id: str) -> list:
        '''Returns a list of past messages in the current channel. The channel must be already subscribed to.'''

        return Messaging.__subscribed_channels[channel_id][0] or [] # TODO: change based on cache eviction policy

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
        
        # return messages TODO: better error handling and documentation
        try:
            return list(res.json())[::-1]
        except:
            return []

    @staticmethod
    def __create_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # add message to cache
            channel_id[0].append(message_data)
            channel_id[1][message_data.get('id')] = len(channel_id[0]) - 1
            # invoke callback
            channel_id[2]()
            
    @staticmethod
    def __delete_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            index = channel_id[1].get(message_data.get('id'))
            # remove message from cache
            if index:
                del channel_id[0][index]
                del channel_id[1][message_data.get('id')]
                channel_id[2]()

    @staticmethod
    def __edit_message(message_data: dict):
        '''Recieves a message from the websocket.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel_id = Messaging.__subscribed_channels[message_data.get('channel_id')]
            index = channel_id[1].get(message_data.get('id'))
            # update message in cache
            if index:
                channel_id[0][index] = message_data
                channel_id[2]()

    Listener.subscribe_event('MESSAGE_CREATE', __create_message)
    Listener.subscribe_event('MESSAGE_DELETE', __delete_message)
    Listener.subscribe_event('MESSAGE_UPDATE', __edit_message)
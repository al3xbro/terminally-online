import requests
import json
from collections import defaultdict

from auth import auth
from websocket import websocket_listener

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

class Messaging:
    
    # { channel_id: ([messages], callback) }
    subscribed_channels = defaultdict(None)

    @staticmethod
    def subscribe_to_channel(channel_id: str, callback: callable) -> None:
        '''Add a channel to a list of subscribed channels. The callback function is invoked when a new message is recieved.'''

        # check if already subscribed
        if channel_id in Messaging.subscribed_channels:
            return

        # add channel to subscribed channels and populate cache
        Messaging.subscribed_channels[channel_id] = (
            Messaging.__get_message_history(channel_id),
            callback
        )

    @staticmethod
    def get_messages(channel_id: str) -> list:
        '''Returns a list of past messages in the current channel. The channel must be already subscribed to.'''

        return Messaging.subscribed_channels[channel_id] or []

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
            return list(res.json())
        except:
            return []

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
    def recieve_message(message: dict):
        '''Recieves a message from the websocket.'''

        # place message in a subscribed channel, if subscribed to
        

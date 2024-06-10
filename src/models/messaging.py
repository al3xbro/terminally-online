from queue import Queue
import requests
import json
from utils.mlist import MessageList
from models.guilds import Guilds

from auth import auth
from websocket.listener import Listener

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

class Messaging:
    
    # { 
    #     channel_id: (MessageList, users, guild_id)
    # }
    __subscribed_channels = {}
    queue = Queue()

    @staticmethod
    def subscribe_channel(guild_id: str, channel_id: str) -> None:
        '''Add a channel to a list of subscribed channels. The callback function is invoked when a new message is received.'''

        # check if already subscribed
        if channel_id in Messaging.__subscribed_channels:
            return

        # add channel to subscribed channels and populate cache TODO: come up with cache eviction policy
        history = Messaging.__get_message_history(channel_id)

        # add to cache
        Messaging.__subscribed_channels[channel_id] = (MessageList(history), {}, guild_id)
        # get users
        for message in history:
            Messaging.__log_user(channel_id, message['author']['username'])

    @staticmethod
    def get_messages(channel_id: str) -> list:
        '''Returns the list of messages in the current channel. The channel must be already subscribed to.'''

        return Messaging.__subscribed_channels[channel_id][0] # TODO: change based on cache eviction policy
    
    @staticmethod
    def get_users(channel_id: str) -> dict:
        '''Returns the list of users in the current channel. The channel must be already subscribed to.'''

        return Messaging.__subscribed_channels[channel_id][1]

    @staticmethod
    def request_older_messages(channel_id: str) -> None:
        '''Requests old messages from the server before message_id. The channel must be already subscribed to.'''

        # get oldest message in cache
        iterator = iter(Messaging.__subscribed_channels[channel_id][0])
        oldest_message = next(iterator)

        # get history
        history = Messaging.__get_message_history(channel_id, before=oldest_message.get('id'), limit=25)
        
        # get users
        for message in history:
            Messaging.__log_user(channel_id, message['author']['username'])

        # tell the view to add messages
        Messaging.queue.put({
            'type': 'p',
            'data': history
        })

        # add to cache
        for message in history[::-1]:
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
    def delete_message(channel_id: str, message_id: str):
        '''Deletes a message from the channel.'''

        # send request
        res = requests.delete(
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', 
            headers = headers | { 'authorization': auth.get_token() }
        )

        # return status TODO: better error handling and documentation
        if res.status_code == 204:
            return True
        return False
    
    @staticmethod
    def edit_message(channel_id: str, message_id: str, content: str):
        '''Edits a message in the channel.'''

        # send request
        res = requests.patch(
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', 
            headers = headers | { 'authorization': auth.get_token() },
            data = json.dumps({ 'content': content })
        )

        # return status TODO: better error handling and documentation
        if res.status_code == 200:
            return True
        return False
    
    @staticmethod
    def __log_user(channel_id: str, username: str):
        '''Logs a user's nickname, color, and roles in the channel.'''

        if username in Messaging.__subscribed_channels[channel_id][1]:
            return
        
        user = {}

        for guild in Guilds.get_guilds():
            if guild['id'] == Messaging.__subscribed_channels[channel_id][2]:
                for member in guild['members']:
                    if member['user']['username'] == username:

                        user['nick'] = ''
                        user['color'] = 0

                        # set nick
                        if member['nick']:
                            user['nick'] = member['nick']
                        else:
                            user['nick'] = member['user']['display_name']

                        # set color
                        if member['roles'] == []:
                            user['color'] = 0
                            user['roles'] = []
                            Messaging.__subscribed_channels[channel_id][1][username] = user
                            return
                        
                        max_position = 0
                        max_role = {}

                        for role_id in member['roles']:
                            challenging_role = {}
                            for role in guild['roles']:
                                if role['id'] == role_id:
                                    challenging_role = role
                                    break
                            if challenging_role['color'] != 0 and challenging_role['position'] > max_position:
                                max_position = challenging_role['position']
                                max_role = challenging_role
                        user['color'] = max_role['color'] if max_role != {} else 0
                        
                        # set roles
                        user['roles'] = member['roles']

                        Messaging.__subscribed_channels[channel_id][1][username] = user
                        return
                    
                # if user is not found
                user['nick'] = ''
                user['color'] = 0
                user['roles'] = []
                Messaging.__subscribed_channels[channel_id][1][username] = user
                return
            
    @staticmethod
    def __get_message_history(channel_id: str, limit: int = 100, before: str = None) -> list:
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
    def __append_message_list(message_data: dict):
        '''Adds a message to the MessageList and tells view to update.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            channel = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # add message to cache
            channel[0].append(message_data.get('id'), message_data)
            # tell the view to add the message
            Messaging.queue.put({
                'type': 'a', 
                'data': message_data
            })
            
    @staticmethod
    def __delete_message_list(message_data: dict):
        '''Deletes a message from the MessageList and tells view to update.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # remove message from cache
            channel[0].delete(message_data.get('id'))
            # tell the view to remove the message
            Messaging.queue.put({
                'type': 'd', 
                'data': message_data
            })

    @staticmethod
    def __edit_message_list(message_data: dict):
        '''Edits a message from the MessageList and tells view to update.'''

        if message_data.get('channel_id') in Messaging.__subscribed_channels:
            # get record from cache
            channel = Messaging.__subscribed_channels[message_data.get('channel_id')]
            # edit message in cache
            channel[0].edit(message_data.get('id'), message_data)
            # tell the view to edit the message
            Messaging.queue.put({
                'type': 'e', 
                'data': message_data
            })

    Listener.subscribe_event('MESSAGE_CREATE', __append_message_list)
    Listener.subscribe_event('MESSAGE_DELETE', __delete_message_list)
    Listener.subscribe_event('MESSAGE_UPDATE', __edit_message_list)
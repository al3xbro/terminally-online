import requests
import json
from auth import auth

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

def get_message_history(guild_id: str, channel_id: str, limit: int) -> list:
    '''Returns a list of messages in the current channel'''

    # send request
    res = requests.get(url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}', 
                        headers = headers | {
                           'referer': f'https://discord.com/channels/{guild_id}/{channel_id}',
                           'authorization': auth.get_token(),
                        })
    
    # return messages TODO: better error handling and documentation
    try:
        return list(res.json())
    except:
        return []

def send_message(guild_id: str, channel_id: str, content: str):
    '''Sends a message to channel'''

    # send request
    res = requests.post(url = f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                        headers = headers | {
                            'referer': f'https://discord.com/channels/{guild_id}/{channel_id}',
                            'authorization': auth.get_token(),
                        },
                        data = json.dumps({'content': content})
                        )
    
    # return status TODO: better error handling and documentation
    if res.status_code == 200:
        return True
    return False

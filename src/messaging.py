import requests
import json
from websockets.sync.client import connect
import time
import threading

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

# get login token TODO: move to auth.py and change token storage
f = open('token.json', 'r')
token = json.load(f).get('token')
f.close()

def get_message_history(guild_id: str, channel_id: str, limit: int) -> list:
    '''Returns a list of messages in the current channel'''

    # send request
    res = requests.get(url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}', 
                        headers = headers | {
                           'referer': f'https://discord.com/channels/{guild_id}/{channel_id}',
                           'authorization': token,
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
                            'authorization': token,
                        },
                        data = json.dumps({'content': content})
                        )
    
    # return status TODO: better error handling and documentation
    if res.status_code == 200:
        return True
    return False

def heartbeat(interval, ws):
    # TODO: send accurate d value
    print("heartbeat")
    while True:
        time.sleep(interval / 1000)
        ws.send(json.dumps({
            'op': 1,
            'd': None
        }))

def receive_messages(ws):
    while True:
        reply = json.loads(ws.recv())
        try:
            author = reply.get('d').get('author').get('global_name')
            username = reply.get('d').get('author').get('username')
            content = reply.get('d').get('content')
            if content and author:
                print(f'{author} ({username}): {content}')
        except Exception as e:
            pass
        
def connect_websocket():

    # websocket handshake
    ws = connect('wss://gateway.discord.gg/?v=9&encoding=json', max_size=999999999)
    # get hello and heartbeat interval
    reply = json.loads(ws.recv())

    # start heartbeat thread
    interval = reply['d']['heartbeat_interval']
    threading.Thread(target=heartbeat, args=(interval, ws)).start()

    # identify
    ws.send(json.dumps({
        'op': 2,
        'd': {
            'token': token,
            'compress': False,
            'properties': {
                '$os': 'Windows',
                '$browser': 'Chrome',
                '$device': ''
            }
        }
    }))

    # loop to receive messages
    threading.Thread(target=receive_messages, args=(ws)).start()

connect_websocket()
from views.home import HomeView
from views.server import ServerView
from views.channel import ChannelView

'''
THESE ARE TEMPORARY PLACEHOLDER FUNCTIONS TO BE REPLACED LATER
I ALSO DONT KNOW EXACTLY HOW THE REAL FUNCTINOS WILL RETURN SO GG
'''

def get_servers(user_id):
    return ([
        {
            "emojis": [],
            "banner": None,
            "id": "832033238004138004",
            "name": "pppp",
            "preferred_locale": "en-US",
            "roles": [
                {
                    "version": 1682664178590,
                    "unicode_emoji": None,
                    "tags": {},
                    "position": 0,
                    "permissions": "559245648401985",
                    "name": "@everyone",
                    "mentionable": False,
                    "managed": False,
                    "id": "832033238004138004",
                    "icon": None,
                    "hoist": False,
                    "flags": 0,
                    "color": 0
                },
            ],
            "mfa_level": 0,
            "members": [
                {
                    "user": {
                        "username": "15aoba",
                        "public_flags": 64,
                        "id": "283407511133093889",
                        "global_name": "15",
                        "display_name": "15",
                        "discriminator": "0",
                        "bot": False,
                        "avatar_decoration_data": None,
                        "avatar": "9dff75940d766b2cd6d66be337707aa9"
                    },
                    "roles": [],
                    "premium_since": None,
                    "pending": False,
                    "nick": None,
                    "mute": False,
                    "joined_at": "2021-04-14T23:23:02.375000+00:00",
                    "flags": 0,
                    "deaf": False,
                    "communication_disabled_until": None,
                    "avatar": None
                }
            ],
            "system_channel_id": "832033238004138006",
            "lazy": True,
            "channels": [
                {
                    "version": 1676709047036,
                    "type": 4,
                    "position": 0,
                    "permission_overwrites": [],
                    "name": "important",
                    "id": "832033238004138005",
                    "flags": 0
                },
                {
                    "version": 1676709158466,
                    "type": 0,
                    "topic": None,
                    "rate_limit_per_user": 0,
                    "position": 2,
                    "permission_overwrites": [],
                    "parent_id": "832033238004138005",
                    "name": "temp",
                    "last_message_id": "1201816855203807232",
                    "id": "832033238004138006",
                    "flags": 0
                },
            ],
            "region": "deprecated"
        }
    ])


class Console:
    def __init__(self, user_id):
        self.view = HomeView(get_servers(user_id))

    def run(self):
        self.view.draw()
        while True:
            self.view = self.view.handle_input()
            self.view.draw()

c = Console(1)
c.run()


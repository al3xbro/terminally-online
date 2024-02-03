import os

from views.view import View

'''
THESE ARE TEMPORARY PLACEHOLDER FUNCTIONS TO BE REPLACED LATER
I ALSO DONT KNOW EXACTLY HOW THE REAL FUNCTINOS WILL RETURN SO GG
'''

def get_messages(channel_id):
    return ([
        {
            "id": "1202006559136428092",
            "type": 0,
            "content": "ok bet",
            "channel_id": "1089098339540291627",
            "author": {
                "id": "283407511133093889",
                "username": "15aoba",
                "avatar": "9dff75940d766b2cd6d66be337707aa9",
                "discriminator": "0",
                "public_flags": 64,
                "premium_type": 2,
                "flags": 64,
                "banner": None,
                "accent_color": None,
                "global_name": "15",
                "avatar_decoration_data": None,
                "banner_color": None
            },
            "attachments": [],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "timestamp": "2024-01-30T21:44:55.900000+00:00",
            "edited_timestamp": None,
            "flags": 0,
            "components": []
        },
        {
            "id": "1202006496855212112",
            "type": 0,
            "content": "6:30",
            "channel_id": "1089098339540291627",
            "author": {
                "id": "735656344966660147",
                "username": "stirfri3d",
                "avatar": "1e3e0a18b8880ed20ecac68bdbe70b2b",
                "discriminator": "0",
                "public_flags": 128,
                "premium_type": 0,
                "flags": 128,
                "banner": None,
                "accent_color": None,
                "global_name": "Glyzz",
                "avatar_decoration_data": None,
                "banner_color": None
            },
            "attachments": [],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "timestamp": "2024-01-30T21:44:41.051000+00:00",
            "edited_timestamp": None,
            "flags": 0,
            "components": []
        },
        {
            "id": "1202006073436012604",
            "type": 0,
            "content": "when is boba",
            "channel_id": "1089098339540291627",
            "author": {
                "id": "283407511133093889",
                "username": "15aoba",
                "avatar": "9dff75940d766b2cd6d66be337707aa9",
                "discriminator": "0",
                "public_flags": 64,
                "premium_type": 2,
                "flags": 64,
                "banner": None,
                "accent_color": None,
                "global_name": "15",
                "avatar_decoration_data": None,
                "banner_color": None
            },
            "attachments": [],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "timestamp": "2024-01-30T21:43:00.100000+00:00",
            "edited_timestamp": None,
            "flags": 0,
            "components": []
        }
    ])


class ChannelView(View):
    def __init__(self, prev_view, channel_id):
        super().__init__()
        self.prev_view = prev_view
        self.channel_id = channel_id
        self.messages = get_messages(channel_id)

    def draw(self):
        os.system('clear')
        for message in self.messages:
            print(f'<{message["author"]["username"]}> {message["content"]}')
        for _ in range(self.height - len(self.messages) - 1):
            print()

    def handle_input(self):
        user_input = input()
        if user_input[:3] == 'cd ':
            if user_input[3:] == '..':
                return self.prev_view
        return self
import os

from views.view import View
from views.channel import ChannelView

class ServerView(View):
    def __init__(self, prev_view, channel_data):
        super().__init__()
        self.prev_view = prev_view
        self.channel_data = channel_data
        self.channel_names = [channel["name"] for channel in channel_data]

    def draw(self):
        os.system('clear')
        for channel in self.channel_names:
            print(f' > {channel}')
        for _ in range(self.height - len(self.channel_names) - 1):
            print()

    def handle_input(self) -> View:
        user_input = input()
        if user_input[:3] == 'cd ':
            if user_input[3:] == '..':
                return self.prev_view
            for channel in self.channel_data:
                if user_input[3:] == channel["name"]:
                    return ChannelView(self, channel["id"])
        return self
                
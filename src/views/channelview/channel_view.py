from textual.screen import Screen
from textual.widgets import Header, Footer

from views.channelview.chat import Chat
from views.channelview.input import ChatInput

class ChannelView(Screen):

    def __init__(self, guild_id: str, channel_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_id = guild_id
        self.channel_id = channel_id

    def compose(self):
        yield Header()
        yield Chat(self.guild_id, self.channel_id)
        yield ChatInput(self.channel_id)
        yield Footer()
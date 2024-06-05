from textual.widgets import Label, Static
from textual.reactive import reactive
from textual.containers import Horizontal
from textual.color import Color
from datetime import datetime

class Message(Static):

    message = reactive('', recompose=True)

    def __init__(self, message, nick, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.nick = nick
        self.color = color

    def delete(self):
        self.query_one('.content').add_class('deleted')

    def update_content(self, message: dict):
        self.message = message

    def decimal_to_rgb(self, decimal_color):
        hex_color = "{:06x}".format(decimal_color)
        colors = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return Color(colors[0], colors[1], colors[2])

    def compose(self):
        username = Label(f"{self.nick} ({self.message['author']['username']}): ", classes='username')
        username.styles.color = self.decimal_to_rgb(self.color)

        with Horizontal(classes='message'):
            yield username
            yield Label(self.message['content'], classes='content')
            yield (Label(' (edited)', classes='edited') if self.message.get('edited_timestamp') else Label(''))
            yield Label(datetime.fromisoformat(self.message['timestamp']).strftime('%m-%d-%Y %H:%M:%S'), classes='timestamp')

        
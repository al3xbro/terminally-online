from textual.widgets import Label, Static, Markdown, TextArea
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
        name = Label(f"{self.nick if self.nick else self.message['author']['username']}: ", classes='username')
        name.styles.color = self.decimal_to_rgb(self.color)

        with Horizontal(classes='message'):
            with Horizontal(classes='message-content'):
                yield name
                yield Label(self.message['content'] + (' (edited)' if self.message.get('edited_timestamp') else ''), classes='content', shrink=True)
            yield Label(datetime.fromisoformat(self.message['timestamp']).strftime('%m-%d-%Y %H:%M:%S'), classes='timestamp')

        
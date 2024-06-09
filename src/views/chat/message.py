from textual import on
from textual.widgets import Label, Static, Button
from textual.reactive import reactive
from textual.containers import Horizontal
from textual.color import Color
from datetime import datetime
from models.messaging import Messaging
from models.user import User

class Message(Static):

    show_options = reactive(False, recompose=True)
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
    
    def parse_timestamp(self, timestamp):
        return datetime.fromisoformat(timestamp).astimezone().strftime('%m-%d-%Y %H:%M:%S')
    
    def on_enter(self):
        self.show_options = True

    def on_leave(self):
        self.show_options = False
    
    def compose(self):
        name = Label(f"{self.nick if self.nick else self.message['author']['username']}:", classes='username')
        name.styles.color = self.decimal_to_rgb(self.color)

        delete = Button('d', classes='delete_button')
        edit = Button('e', classes='edit_button')
        reply = Button('r', classes='reply_button')

        @on(Button.Pressed, '.delete_button')
        def delete_message():
            Messaging.delete_message(self.message['id'])

        with Horizontal(classes='message'):
            with Horizontal(classes='message-content'):
                yield name
                yield Label((self.message['content'] if 'content' in self.message else '') + 
                            (' (edited)' if self.message.get('edited_timestamp') else ''),
                              classes='content', shrink=True
                )
            yield (Horizontal(reply, edit, delete, classes='options') if self.message['author']['username'] == User.get_username() else Horizontal(reply, classes='options')) if self.show_options else Label(self.parse_timestamp(self.message['timestamp']), classes='timestamp')              
from textual import on
from textual.widgets import Label, Button
from textual.reactive import reactive
from textual.containers import Horizontal
from textual.color import Color
from datetime import datetime
from models.messaging import Messaging
from models.user import User

class Message(Horizontal):

    message = reactive('', recompose=True)
    deleted = reactive(False, recompose=True)

    def __init__(self, message, nick, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.nick = nick
        self.color = color

    def delete(self):
        self.deleted = True

    def update_content(self, message: dict):
        self.message = message

    def decimal_to_rgb(self, decimal_color):
        hex_color = "{:06x}".format(decimal_color)
        colors = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return Color(colors[0], colors[1], colors[2])
    
    def parse_timestamp(self, timestamp):
        return datetime.fromisoformat(timestamp).astimezone().strftime('%H:%M:%S')
    
    def is_mention(self):
        for mention in self.message['mentions']:
            if mention['username'] == User.get_username():
                return True
        for role_id in self.message['mention_roles']:
            if role_id in Messaging.get_users(self.message['channel_id'])[User.get_username()]['roles']:
                return True
        return self.message['mention_everyone']
    
    @on(Button.Pressed, '.delete_button')
    def on_delete(self):
        Messaging.delete_message(self.message['channel_id'], self.message['id'])

    def compose(self):
        name = Label(f"{self.nick if self.nick else self.message['author']['username']}:", classes='username')
        name.styles.color = self.decimal_to_rgb(self.color)

        content = Label((self.message['content'] if 'content' in self.message else '') + 
                        (' (edited)' if self.message.get('edited_timestamp') else ''),
                            classes='content', shrink=True)
        if self.deleted: content.add_class('deleted')
        if self.is_mention(): content.add_class('highlight')

        reply = Button('r', classes='reply_button')
        edit = Button('e', classes='edit_button')
        delete = Button('d', classes='delete_button')

        with Horizontal(classes='message_content'):
            yield name
            yield content
        with Horizontal(classes='message_options'):
            yield (Horizontal(delete, edit, reply, classes='options') if self.message['author']['username'] == User.get_username() else Horizontal(reply, classes='options'))
            yield Label(self.parse_timestamp(self.message['timestamp']), classes='timestamp')              
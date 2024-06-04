from textual.widgets import Label, Static
from textual.reactive import reactive
from textual.containers import Horizontal
from datetime import datetime

class Message(Static):

    message = reactive('', recompose=True)

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def delete(self):
        c = self.query_one('.content')
        c.add_class('deleted')
        print('bruh')

    def update_content(self, content: str):
        self.message = { **self.message, 'content': content }

    def compose(self):
        with Horizontal():
            yield Label(f"{self.message['author']['username']}:", classes='username')
            yield Label(self.message['content'], classes='content')
            yield (Label(' (edited)', classes='edited') if self.message.get('edited_timestamp') else Label(''))
            yield Label(datetime.fromisoformat(self.message['timestamp']).strftime('%m-%d-%Y %H:%M:%S'), classes='timestamp')
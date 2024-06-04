from textual.widgets import Label, Static
from textual.reactive import reactive
from textual.containers import Horizontal

class Message(Static):

    message = reactive('', recompose=True)

    def __init__(self, message, id):
        super().__init__(id=id)
        self.message = message

    def update_content(self, content: str):
        print('update')
        self.message = { **self.message, 'content': content }

    def compose(self):
        with Horizontal():
            yield Label(f"{self.message['author']['username']}:", classes='username')
            yield Label(self.message['content'], classes='content')
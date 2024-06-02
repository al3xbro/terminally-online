from textual.widgets import Label, Static
from textual.containers import Horizontal

class Message(Static):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def compose(self):
        with Horizontal():
            yield Label(f"{self.message['author']['username']}:", classes='username')
            yield Label(self.message['content'], classes='content')
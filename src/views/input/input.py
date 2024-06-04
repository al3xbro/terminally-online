from textual import work
from textual.widgets import Input, Static
from models.messaging import Messaging

class ChatInput(Input):

    channel_id = None

    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.placeholder = 'Enter your message here'

    async def submit_message(self, value):
        Messaging.send_message(self.channel_id, value)

    def on_input_submitted(self):
        self.run_worker(self.submit_message(self.value))
        self.value = ''

from textual.widgets import Input
from models.messaging import Messaging

class ChatInput(Input):

    # TODO: add edit, reply modes
    channel_id = None

    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.placeholder = 'Enter your message here'

    async def submit_message(self, value):
        Messaging.send_message(self.channel_id, value)

    def on_input_submitted(self):
        value = self.value
        self.value = ''
        self.run_worker(self.submit_message(value))
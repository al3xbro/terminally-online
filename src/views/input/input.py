from textual.widgets import Input, Static
from models.messaging import Messaging

class CommandInput(Input):

    channel_id = None

    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.placeholder = 'Enter your message here'

    def on_input_submitted(self):
        if (Messaging.send_message(self.channel_id, self.value)):
            print('sent')
        self.value = ''

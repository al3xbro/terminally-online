from textual.widgets import Label
from models.messaging import Messaging

class EditButton(Label):
    
    def __init__(self, message, *args, **kwargs):
        super().__init__(renderable='e' *args, **kwargs)

    def on_click(self):
        Messaging.edit_message(self.message['channel_id'], self.message['id'])
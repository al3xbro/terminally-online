from textual.widgets import Label
from models.messaging import Messaging

class DeleteButton(Label):
    
    def __init__(self, message, *args, **kwargs):
        super().__init__(renderable='x', classes='delete_button', *args, **kwargs)
        self.message = message

    def on_click(self):
        Messaging.delete_message(self.message['channel_id'], self.message['id'])
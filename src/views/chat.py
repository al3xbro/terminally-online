from textual.containers import VerticalScroll
from views.message import Message
from models.messaging import Messaging

class Chat(VerticalScroll):

    def __init__(self, channel: str):
        super().__init__()
        self.channel = channel
        Messaging.subscribe_channel(self.channel)
        self.messages = Messaging.get_messages(self.channel)

    def check_for_updates(self):
        try:
            update = Messaging.queue.get_nowait()
            if update['type'] == 'a':
                self.create_message(update['data'])
            elif update['type'] == 'p':
                self.refresh(recompose=True)
            elif update['type'] == 'd':
                self.delete_message(update['data'])
            elif update['type'] == 'e':
                self.edit_message(update['data'])
        except:
            pass

    def create_message(self, message: dict):
        self.mount(Message(message, id = f'message-{message["id"]}'))
        self.scroll_end(animate=False)

    def delete_message(self, message: dict):
        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.delete()

    def edit_message(self, message: dict):
        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.update_content(message['content'])

    def on_mount(self):
        for message in iter(self.messages):
            self.mount(Message(message, id = f'message-{message["id"]}'))
        self.set_interval(0.1, self.check_for_updates)
        self.scroll_end(animate=False)
        self.visible = True
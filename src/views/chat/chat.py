from textual.containers import VerticalScroll
from textual.events import MouseScrollUp
from views.chat.message import Message
from models.messaging import Messaging

class Chat(VerticalScroll):

    scroll_enabled = True

    def __init__(self, guild_id: str,  channel_id: str):
        super().__init__()
        self.guild_id = guild_id
        self.channel_id = channel_id
        Messaging.subscribe_channel(self.guild_id, self.channel_id)
        self.messages = Messaging.get_messages(self.channel_id)

    def check_for_updates(self):
        '''Checks for updates in the queue. If there is an update, it will process it.'''

        try:
            update = Messaging.queue.get_nowait()
            if update['type'] == 'a':
                self.create_message(update['data'])
            elif update['type'] == 'p':
                self.prepend_messages(update['data'])
            elif update['type'] == 'd':
                self.delete_message(update['data'])
            elif update['type'] == 'e':
                self.edit_message(update['data'])
        except:
            pass
              
    def create_message(self, message: dict):
        '''Adds a message to the chat.'''

        self.mount(Message(message, Messaging.get_users(self.channel_id)[message['author']['username']]['nick'], Messaging.get_users(self.channel_id)[message['author']['username']]['color'], id = f'message-{message["id"]}'))
        if self.scrollable_content_region.height - self.scroll_offset.y < 10:
            self.scroll_end(animate=True)

    def delete_message(self, message: dict):
        '''Deletes a message from the chat.'''

        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.delete()

    def edit_message(self, message: dict):
        '''Edits a message in the chat.'''

        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.update_content(message)

    def prepend_messages(self, messages: list): 
        '''Prepends messages to the chat.'''

        self.mount_all([Message(message, Messaging.get_users(self.channel_id)[message['author']['username']]['nick'], Messaging.get_users(self.channel_id)[message['author']['username']]['color'], id = f'message-{message["id"]}') for message in messages], before=0)
        self.scroll_enabled = True

    def action_scroll_up(self) -> None:
        '''Scrolls up in the chat. If the scroll offset is 0, it will request older messages.'''

        if not self.scroll_enabled:
            return
        if self.scroll_offset.y == 0:
            self.scroll_enabled = False
            Messaging.request_older_messages(self.channel_id)
            self.scroll_to(0, 24, animate=False) 
            self.set_timer(1, lambda: setattr(self, 'scroll_enabled', True))
        else:
            super().action_scroll_up()
    
    def _on_mouse_scroll_up(self, event: MouseScrollUp) -> None:
        '''Scrolls up in the chat. If the scroll offset is 0, it will request older messages.'''

        if not self.scroll_enabled:
            return
        if self.scroll_offset.y == 0:
            self.scroll_enabled = False
            Messaging.request_older_messages(self.channel_id)
            self.scroll_to(0, 24, animate=False)
            self.set_timer(1, lambda: setattr(self, 'scroll_enabled', True))
        else:
            super()._on_mouse_scroll_up(event)
    
    async def on_mount(self):
        for message in iter(self.messages):
            self.create_message(message)
        self.set_interval(0.1, self.check_for_updates)
        self.scroll_end(animate=False)
        Messaging.request_older_messages(self.channel_id)
from textual.containers import VerticalScroll
from textual.events import MouseScrollUp
from textual.scrollbar import ScrollUp
from models.guilds import Guilds
from views.chat.message import Message
from models.messaging import Messaging

class Chat(VerticalScroll):

    # TODO: move to messaging model
    users = {}
    scroll_enabled = True

    def __init__(self, guild: str,  channel: str):
        super().__init__()
        self.guild = guild
        self.channel = channel
        Messaging.subscribe_channel(self.channel)
        self.messages = Messaging.get_messages(self.channel)

    def check_for_updates(self):
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

    def log_user(self, username: str):
        self.users[username] = {}

        for guild in Guilds.get_guilds():
            if guild['id'] == self.guild:
                for member in guild['members']:
                    if member['user']['username'] == username:
                        # set nick
                        nick = ''
                        if member['nick']:
                            nick = member['nick']
                        else:
                            nick = member['user']['display_name']

                        # set color
                        if member['roles'] == []:
                            Guilds.guilds[guild['name']]['members'][member['user']['username']]['color'] = 0
                            continue
                        
                        max_position = 0
                        max_role = {}

                        for role_id in member['roles']:
                            challenging_role = {}
                            for role in guild['roles']:
                                if role['id'] == role_id:
                                    challenging_role = role
                                    break
                            if challenging_role['color'] != 0 and challenging_role['position'] > max_position:
                                max_position = challenging_role['position']
                                max_role = challenging_role
                        self.users[username]['nick'] = nick
                        self.users[username]['color'] = max_role['color']
                        return
                    
                # member does not exist
                self.users[username]['nick'] = username
                break
                    
    def create_message(self, message: dict):
        try:
            if message['author']['username'] not in self.users:
                self.log_user(message['author']['username'])
            self.mount(Message(message, self.users[message['author']['username']]['nick'], self.users[message['author']['username']]['color'], id = f'message-{message["id"]}'))
            print(self.scrollable_content_region.height, self.scroll_offset.y)
            if self.scrollable_content_region.height - self.scroll_offset.y < 10:
                self.scroll_end(animate=True)
        except:
            self.mount(Message(message, '', 0, id = f'message-{message["id"]}'))

    def delete_message(self, message: dict):
        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.delete()

    def edit_message(self, message: dict):
        old_message = self.query_one(f'#message-{message["id"]}')
        old_message.update_content(message)

    def prepend_messages(self, messages: list): 
        for message in messages:
            if message['author']['username'] not in self.users:
                self.log_user(message['author']['username'])
        self.mount_all([Message(message, self.users[message['author']['username']]['nick'], self.users[message['author']['username']]['color'], id = f'message-{message["id"]}') for message in messages], before=0)

    # FIXME: a few seconds after load, request doesnt work
    def action_scroll_up(self) -> None:
        if not self.scroll_enabled:
            return
        if self.scroll_offset.y == 0:
            self.scroll_enabled = False
            Messaging.request_older_messages(self.channel)
            self.scroll_to(0, 24, animate=False) 
            self.set_timer(1, lambda: setattr(self, 'scroll_enabled', True))
        else:
            super().action_scroll_up()
    
    def _on_mouse_scroll_up(self, event: MouseScrollUp) -> None:
        if not self.scroll_enabled:
            return
        if self.scroll_offset.y == 0:
            self.scroll_enabled = False
            Messaging.request_older_messages(self.channel)
            self.scroll_to(0, 24, animate=False)
            self.set_timer(1, lambda: setattr(self, 'scroll_enabled', True))
        else:
            super()._on_mouse_scroll_up(event)
    
    async def on_mount(self):
        for message in iter(self.messages):
            self.create_message(message)
        self.set_interval(0.1, self.check_for_updates)
        self.scroll_end(animate=False)
        Messaging.request_older_messages(self.channel)
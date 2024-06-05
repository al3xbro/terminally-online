from textual.containers import VerticalScroll
from textual.scrollbar import ScrollUp
from models.guilds import Guilds
from views.chat.message import Message
from models.messaging import Messaging

class Chat(VerticalScroll):

    users = {}

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
                        elif member['user']['display_name']:
                            nick = member['user']['display_name']
                        else:
                            nick = member['user']['username']

                        # set color
                        if member['roles'] == []:
                            Guilds.guilds[guild['name']]['members'][member['user']['username']]['color'] = 0
                            continue
                        
                        max_role = {}
                        for role in guild['roles']:
                            if role['id'] == member['roles'][0]:
                                max_role = role
                                break

                        for role_id in member['roles']:
                            challenging_role = {}
                            for role in guild['roles']:
                                if role['id'] == role_id:
                                    challenging_role = role
                                    break
                            if challenging_role['position'] > max_role['position']:
                                max_role = challenging_role
                        self.users[username]['nick'] = nick
                        self.users[username]['color'] = max_role['color']
                        return
                    
    def create_message(self, message: dict):
        if message['author']['username'] not in self.users:
            self.log_user(message['author']['username'])
        try:
            self.mount(Message(message, self.users[message['author']['username']]['nick'], self.users[message['author']['username']]['color'], id = f'message-{message["id"]}'))
        except:
            self.mount(Message(message, '', 0, id = f'message-{message["id"]}'))
        self.scroll_end(animate=False)

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
        self.scroll_to(0, 49, animate=False)

    def action_scroll_up(self) -> None:
        if self.scroll_offset.y == 0:
            Messaging.request_older_messages(self.channel)
        return super().action_scroll_up()
    
    async def on_mount(self):
        for message in iter(self.messages):
            self.create_message(message)
        self.set_interval(0.1, self.check_for_updates)
        self.scroll_end(animate=False)
        Messaging.request_older_messages(self.channel)
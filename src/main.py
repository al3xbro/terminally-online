import time
from textual.app import App
from auth import auth
from views.chat.chat import Chat
from views.input.chat_input import ChatInput
from textual.widgets import Header, Footer
from websocket.listener import Listener

class TerminallyOnline(App):

    CSS_PATH = 'style.tcss'
    guild_id = '1184053178380079175'
    channel_id = '1184053178975662192'

    def compose(self):
        yield Header()
        yield Chat(self.guild_id, self.channel_id)
        yield ChatInput(self.channel_id)
        yield Footer()

if __name__ == '__main__':
    while not Listener.ready:
        time.sleep(0.1)
    
    while not auth.logged_in():
        print('u need to login.')
        email = input('enter email: ')
        pw = input('enter pw: ')
        mfa = input('enter mfa (enter if none): ')
        status = auth.login(email, pw, mfa if mfa != '' else None)
        if (status != auth.LoginStatus.SUCCESS):
            print('login failed.', status, '\n')
        
    app = TerminallyOnline()
    app.run()
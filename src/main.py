import time
from textual.app import App
from auth import auth
from views.channelview.channel_view import ChannelView
from views.commandview.command_view import CommandView
from websocket.listener import Listener


class TerminallyOnline(App):

    guild_id = '1184053178380079175'
    channel_id = '1184053178975662192'

    CSS_PATH = 'style.tcss'

    SCREENS = {
        'channel_view': ChannelView(guild_id, channel_id),
        'command_view': CommandView()
    }

    def on_mount(self):
        self.push_screen('command_view')


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
from textual.app import App
from auth import auth
from views.chat.chat import Chat
from views.input.input import ChatInput
from textual.widgets import Header

class TerminallyOnline(App):

    CSS_PATH = 'style.tcss'
    channel_id = '1089098339540291627'


    def compose(self):
        yield Header()
        yield Chat(self.channel_id)
        yield ChatInput(self.channel_id)

if __name__ == '__main__':

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
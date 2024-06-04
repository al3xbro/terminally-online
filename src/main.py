from textual.app import App
from views.chat.chat import Chat
from views.input.input import CommandInput
from textual.widgets import Header

class TerminallyOnline(App):

    CSS_PATH = 'style.tcss'
    channel_id = '1089098339540291627'

    def compose(self):
        yield Header()
        yield Chat(self.channel_id)
        yield CommandInput(self.channel_id)

if __name__ == '__main__':
    app = TerminallyOnline()
    app.run()
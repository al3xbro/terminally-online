from textual.app import App
from views.chat import Chat
from textual.widgets import Header

class TerminallyOnline(App):

    CSS_PATH = 'style.tcss'

    def compose(self):
        yield Header()
        yield Chat('1184053178975662192')

if __name__ == '__main__':
    app = TerminallyOnline()
    app.run()
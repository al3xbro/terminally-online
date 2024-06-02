from textual.app import App
from models.messaging import Messaging
from views.message import Message
from textual.containers import VerticalScroll
from textual.widgets import Header

class TerminallyOnline(App):

    CSS_PATH = 'style.tcss'

    def __init__(self):
        self.channel = '832033238004138006'
        Messaging.subscribe_channel(self.channel, self.display_new)
        self.messages = Messaging.get_messages(self.channel)
        super().__init__()

    # i want to call this method whenever a new message is received. this should update my chat log
    def display_new(self):
        self.refresh(recompose=True)
        self.call_after_refresh(self.scroll_to_end)

    def scroll_to_end(self):
        self.query_one('#scrollable').scroll_end(animate=False)

    def on_mount(self):
        self.scroll_to_end()

    def compose(self): 
        yield Header()
        iterator = iter(self.messages)
        with VerticalScroll(id='scrollable'):
            for message in iterator:
                yield Message(message)
        

if __name__ == '__main__':
    app = TerminallyOnline()
    app.run()
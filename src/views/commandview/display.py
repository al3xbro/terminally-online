from textual.widgets import Label
from rich.text import Text
from models.user import User
from textual.containers import VerticalScroll

class Display(VerticalScroll):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_prompt(self, path: list):
        renderable = Text()
        renderable.append(User.get_username() + '@TerminallyOnline', style='bold green')
        renderable.append(':', style='bold')
        renderable.append('~/' + '/'.join(path), style='bold blue')
        renderable.append('$ ', style='bold')
        self.mount(Label(renderable, classes='prompt'))
        self.scroll_end()

    def remove_prompt(self):
        self.remove_children('.prompt')

    def add_command(self, path: list, text: str):
        renderable = Text()
        renderable.append(User.get_username() + '@TerminallyOnline', style='bold green')
        renderable.append(':', style='bold')
        renderable.append('~/' + '/'.join(path), style='bold blue')
        renderable.append('$ ', style='bold')
        renderable.append(text)
        self.mount(Label(renderable))
        self.scroll_end()

    def add_info(self, renderable):
        self.mount(Label(renderable))
        self.scroll_end()

    def add_err(self, text: str):
        renderable = Text()
        renderable.append('TerminallyOnline: ')
        renderable.append(text)
        self.mount(Label(renderable))
        self.scroll_end()

    def clear(self):
        self.remove_children()

    def on_mount(self):
        self.scroll_end()


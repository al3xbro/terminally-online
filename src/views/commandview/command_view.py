from textual.screen import Screen
from textual.widgets import Header, Footer
from views.commandview.input import CommandInput
from views.commandview.display import Display

class CommandView(Screen):

    path = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Header()
        yield Display()
        yield CommandInput()
        yield Footer()
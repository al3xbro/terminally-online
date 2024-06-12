from textual.widgets import Input
from models.guilds import Guilds

class CommandInput(Input):

    path = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = 'Enter your command here'
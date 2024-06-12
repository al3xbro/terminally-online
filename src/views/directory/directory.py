from textual.widgets import Label
from models.guilds import Guilds

class Directory(Label):
    
    path = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
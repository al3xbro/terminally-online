from textual.widgets import Label
from textual.containers import VerticalScroll
from models.guilds import Guilds

class Display(VerticalScroll):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

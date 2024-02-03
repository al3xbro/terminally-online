import os

class View:
    def __init__(self):
        self.width, self.height = os.get_terminal_size()
        
    def draw(self):
        pass

    def handle_input(self):
        pass
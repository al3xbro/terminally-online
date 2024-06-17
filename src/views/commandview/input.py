from textual.widgets import Input

class CommandInput(Input):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = 'Enter your command here'

    def on_input_submitted(self):
        self.parent.parse_command(self.value)
        self.value = ''
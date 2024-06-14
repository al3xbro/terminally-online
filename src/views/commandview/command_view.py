from textual.screen import Screen
from textual.widgets import Header, Footer
from views.commandview.input import CommandInput
from views.commandview.display import Display
import sys
import threading

class CommandView(Screen):

    display = Display()
    path = []

    def __init__(self, *command, **kwcommand):
        super().__init__(*command, **kwcommand)

    def parse_command(self, value):
        '''Possible commands: cd, ls, quit/exit/, logout, clear, help.
           Possible errors: invalid command, too many arguments, too few arguments
        '''

        command = value.split(' ')

        match command[0]:
            case 'cd':
                self.command_cd(command)
            case 'ls':
                self.command_ls(command)
            case 'quit', 'exit':
                self.command_quit(command)
            case 'logout':
                self.command_logout(command)
            case 'clear':
                self.command_clear(command)
            case 'help':
                self.command_help(command)
            case _:
                self.command_not_found(command)

    def command_cd(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))

    def command_ls(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))

    def command_quit(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))
        threading.exit()
        sys.exit()

    def command_logout(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))

    def command_clear(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))

    def command_help(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))
    
    def command_not_found(self, command):
        self.display.add_command('/' + '/'.join(self.path), ' '.join(command))

    def compose(self):
        yield Header()
        yield self.display
        yield CommandInput()
        yield Footer()
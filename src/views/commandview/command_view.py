from textual.screen import Screen
from textual.widgets import Header, Footer
from views.commandview.input import CommandInput
from views.commandview.display import Display
from models.guilds import Guilds
import sys
import threading

class CommandView(Screen):

    guild_dirview = Guilds.guilds_dirview
    display = Display()
    path = []

    def __init__(self, *command, **kwcommand):
        super().__init__(*command, **kwcommand)

    def parse_command(self, value: str):
        '''Possible commands: cd, ls, quit/exit, logout, clear, help.
           Possible errors: invalid command, too many arguments, too few arguments
        '''

        if value.strip() == '':
            return

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

        self.display.add_prompt(self.path)

    def command_cd(self, command):
        if len(command) > 2:
            self.display.remove_prompt()
            self.display.add_command(self.path, ' '.join(command))
            self.display.add_err('cd: too many arguments')
            return

        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))
        potential_path = []
        if len(command) == 1 or command[1] == '~':
            pass
        elif command[1].startswith('~/'):
            potential_path = command[1][2:].split('/')
        elif command[1].startswith('./'):
            potential_path = self.path + command[1][2:].split('/')
        else:
            potential_path = self.path + command[1].split('/')
        
        # validate path and respond here
        self.display.add_info('going to ' + str(potential_path))

    def command_ls(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))

    def command_quit(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))
        threading.exit()
        sys.exit()

    def command_logout(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))

    def command_clear(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))

    def command_help(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))
    
    def command_not_found(self, command):
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))

    def open_channel(self, path):
        self.display.remove_prompt()
        self.display.add_command(self.path, path)

    def on_mount(self):
        self.display.remove_prompt()
        self.display.add_prompt(self.path)

    def compose(self):
        yield Header()
        yield self.display
        yield CommandInput()
        yield Footer()
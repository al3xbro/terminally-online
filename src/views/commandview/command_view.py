from textual.screen import Screen
from textual.widgets import Header, Footer
from views.commandview.input import CommandInput
from views.commandview.display import Display
from models.guilds import Guilds
import sys
import threading

class CommandView(Screen):

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

        command = value.strip().split(' ')

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
        self.display.remove_prompt()
        self.display.add_command(self.path, ' '.join(command))

        if len(command) > 2:
            self.display.add_err('cd: too many arguments')
            return

        potential_path = []

        # parse directory
        if len(command) == 1:
            potential_path = ['~']
        else:
            potential_path = command[1].split('/')

        # if relative path, add current path
        if potential_path[0] != '~':
            potential_path = self.path + potential_path
        else:
            potential_path = potential_path[1:]

        parsed_path = []
        
        for f in potential_path:
            
            if f == '..' and len(parsed_path) > 0:
                parsed_path.pop()
            elif f == '.':
                continue
            else: 
                parsed_path.append(f)

        current_path = Guilds.guilds_dirview

        # test if path exists
        for f in parsed_path:
            found = False
            for c in current_path:
                if c['name'] == f:
                    found = True
                    if 'subdirectories' not in c:
                        print(c)
                        self.display.add_err(f'cd: {command[1]}: Not a directory')
                        return
                    current_path = c['subdirectories']
                    break
            if not found:
                self.display.add_err(f'cd: {command[1]}: No such file or directory')
                return

        # update path
        self.path = parsed_path

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
from textual.screen import Screen
from textual.widgets import Header, Footer
from views.channelview.channel_view import ChannelView
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
        self.display.remove_prompt()
        self.display.add_command(self.path, value)

        '''Possible commands: cd, ls, quit/exit, logout, clear, help.
           Possible errors: invalid command, too many arguments, too few arguments
        '''

        if value.strip() == '':
            return

        command = value.strip().split(' ')

        if value.startswith('./'):
            self.open_channel(value[2:])
            self.display.add_prompt(self.path)
            return

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
            self.display.add_err('cd: too many arguments')
            return
        
        # handle 
        parsed_path = []
        if len(command) != 1:
            parsed_path = command[1].split('/')
        else: 
            parsed_path = ['~']

        # update path
        directory = self.get_dir(parsed_path)
        if directory == None:
            self.display.add_err(f'cd: {command[1]}: No such file or directory')
        else:
            if 'subdirectories' in directory[0] or len(directory[1]) == 0:
                self.path = directory[1]
            else:
                self.display.add_err(f'cd: {command[1]}: Not a directory')

    def command_ls(self, command):
        if len(command) > 2:
            self.display.add_err('ls: too many arguments')
            return
        
        parsed_path = []
        if len(command) == 2:
            parsed_path = command[1].split('/')

        directory = self.get_dir(parsed_path)
        if directory == None:
            self.display.add_err(f'ls: {command[1]}: No such file or directory')
        else:
            if 'subdirectories' in directory[0]:
                res = ''
                for c in directory[0]['subdirectories']:
                    res += c['name'] + '  '
                self.display.add_info(res)
            else:
                self.display.add_err(f'ls: {command[1]}: Not a directory')

    def command_quit(self, command):
        pass
        threading.exit()
        sys.exit()

    def command_logout(self, command):
        pass

    def command_clear(self, command):
        pass

    def command_help(self, command):
        pass
    
    def command_not_found(self, command):
        self.display.add_err(f'{command[0]}: command not found')

    def open_channel(self, path):
        directory = self.get_dir(path.split('/'))
        if directory == None:
            self.display.add_err(f'./{path}: No such file or directory')
        else:
            if 'subdirectories' in directory[0]:
                self.display.add_err(f'./{path}: Is a directory')
            else:
                if not self.app.is_screen_installed(f'channel_view_{directory[0]["id"]}'):
                    self.app.install_screen(ChannelView(directory[0]['guild_id'], directory[0]['id']), f'channel_view_{directory[0]["id"]}')
                self.app.push_screen(f'channel_view_{directory[0]["id"]}')

    def on_mount(self):
        self.display.remove_prompt()
        self.display.add_prompt(self.path)

    def compose(self):
        yield Header()
        yield self.display
        yield CommandInput()
        yield Footer()

    def get_dir(self, path: list[str]):
        '''Returns a tuple with the directory and the parsed path. Takes relative and absolute paths.'''

        # if relative path, add current path
        if len(path) == 0 or path[0] != '~':
            path = self.path + path
        else:
            path = path[1:]

        parsed_path = []
        
        for f in path:
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
            if 'subdirectories' not in current_path:
                return None
            for c in current_path['subdirectories']:
                if c['name'] == f:
                    found = True
                    current_path = c
                    break
            if not found:
                return None
            
        return (current_path, parsed_path)
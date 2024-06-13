from textual.widgets import Input
from models.guilds import Guilds

class CommandInput(Input):

    current_path = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = 'Enter your command here'

    def parse_command(self):
        '''Possible commands: cd, ls, quit/exit/, logout, clear, help.
           Possible errors: invalid command, too many arguments, too few arguments
        '''

        command = self.value.split(' ')
        self.value = ''

        match command[0]:
            case 'cd':
                if len(command) > 2:
                    print('cd: too many arguments')
                elif len(command) == 2:
                    self.command_cd(command[1])
                else:
                    print('print help here')
            case 'ls':
                if len(command) > 2:
                    print('ls: too many arguments')
                elif len(command) == 2:
                    self.command_ls(command[1])
                else:
                    self.command_ls(self.current_path)
            case 'quit', 'exit':
                if len(command) > 1:
                    print('quit: too many arguments')
                else:
                    self.command_quit()
            case 'logout':
                if len(command) > 1:
                    print('logout: too many arguments')
                else:
                    self.command_logout()
            case 'clear':
                if len(command) > 1:
                    print('clear: too many arguments')
                else:
                    self.command_clear()
            case 'help':
                print('help')
    
    def command_cd(self, path):
        print('cd', path)

    def command_ls(self, path):
        print('ls', path)

    def command_quit(self):
        print('quit')

    def command_logout(self):
        print('logout')

    def command_clear(self):
        print('clear')

    def command_help(self):
        print('help')
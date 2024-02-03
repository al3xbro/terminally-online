import os

from views.view import View
from views.server import ServerView

class HomeView(View):
    def __init__(self, server_data):
        super().__init__()
        self.server_data = server_data
        self.server_names = [server["name"] for server in server_data]
        
    def draw(self):
        os.system('clear')
        for server in self.server_names:
            print(f' > {server}')
        for _ in range(self.height - len(self.server_names) - 1):
            print()

    def handle_input(self) -> View:
        user_input = input()
        if user_input[:3] == 'cd ':
            for server in self.server_data:
                if user_input[3:] == server["name"]:
                    return ServerView(self, server["channels"])
            return self
                

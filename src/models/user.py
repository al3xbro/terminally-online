from websocket.listener import Listener

class User:

    username = None
    user_id = None

    @staticmethod
    def __set_user(data: dict) -> None:
        '''Set the user's username and user_id'''

        User.username = data['user']['username']
        User.user_id = data['user']['id']

    def get_username() -> str:
        '''Returns the user's username'''

        return User.username
    
    def get_user_id() -> str:
        '''Returns the user's user_id'''

        return User.user_id

    Listener.subscribe_event('READY', __set_user)
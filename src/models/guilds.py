from websocket.listener import Listener

class Guilds:
    
    guilds = {}
    private_channels = []
    
    @staticmethod
    def __set_guilds(data: dict) -> None:
        '''Set the guilds'''

        Guilds.guilds = data['guilds']
        Guilds.private_channels = data['private_channels']
    
    @staticmethod
    def get_guilds() -> list:
        '''Returns the guilds'''
        
        return Guilds.guilds
    
    @staticmethod
    def get_private_channels() -> list:
        '''Returns the private channels'''
        
        return Guilds.private_channels
    
    Listener.subscribe_event('READY', __set_guilds)
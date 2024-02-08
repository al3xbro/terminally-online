from websocket.listener import Listener

class Guilds:
    
    guilds = []
    guild_folders = []
    private_channels = []
    
    @staticmethod
    def __set_guilds(data: dict) -> None:
        '''Set the guilds'''
        
        Guilds.guilds = data['guilds']
        Guilds.guild_folders = data['user_settings']['guild_folders']
        Guilds.private_channels = data['private_channels']
    
    def get_guilds() -> list:
        '''Returns the guilds'''
        
        return Guilds.guilds
    
    def get_guild_folders() -> list:
        '''Returns the guild folders'''
        
        return Guilds.guild_folders
    
    def get_private_channels() -> list:
        '''Returns the private channels'''
        
        return Guilds.private_channels
    
    Listener.subscribe_event('READY', __set_guilds)
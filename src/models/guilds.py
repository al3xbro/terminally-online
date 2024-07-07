import json
import sys
from websocket.listener import Listener

class Guilds:
    
    guilds = []
    private_channels = []

    guilds_dirview = {'subdirectories': []}

    @staticmethod
    def __set_guilds(data: dict) -> None:
        '''Set the guilds'''

        Guilds.guilds = data['guilds']
        Guilds.private_channels = data['private_channels']

        for guild in Guilds.guilds:
            
            # create guild
            curr_guild = {
                'id': guild['id'],
                'name': guild['name'],
                'subdirectories': []
            }
            Guilds.guilds_dirview['subdirectories'].append(curr_guild)

            # add categories
            for channel in guild['channels']:
                if channel['type'] == 4:
                    curr_guild['subdirectories'].append({
                        'id': channel['id'],
                        'name': channel['name'],
                        'position': channel['position'],
                        'subdirectories': []
                    })

            # add channels to categories
            for channel in guild['channels']:
                if channel['type'] == 0:
                    min_category = None

                    # find the category it belongs to
                    for category in curr_guild['subdirectories']:
                        if min_category is None:
                            min_category = category
                        elif channel['position'] > category['position'] and category['position'] < min_category['position']:
                            min_category = category

                    # add channel if it is uncategorized
                    if min_category:
                        min_category['subdirectories'].append({
                            'id': channel['id'],
                            'name': channel['name'],
                            'position': channel['position'],
                            'guild_id': guild['id']
                        })
                    # if no category, that means it's uncategorized
                    else:
                        # if there no an uncategorized, make one
                        if len(curr_guild['subdirectories']) == 0 or curr_guild['subdirectories'][0]['name'] != 'uncategorized':
                            curr_guild['subdirectories'].insert(0, {
                                'id': 0,
                                'name': 'uncategorized',
                                'position': -1,
                                'subdirectories': [{
                                    'name': channel['name'],
                                    'position': channel['position']
                                }]
                            })
                        # add channel to uncategorized
                        else:
                            curr_guild['subdirectories'][0].append({
                                'id': channel['id'],
                                'name': channel['name'],
                                'position': channel['position']
                            })
        


    @staticmethod
    def get_guilds() -> list:
        '''Returns the guilds'''
        
        return Guilds.guilds
    
    @staticmethod
    def get_private_channels() -> list:
        '''Returns the private channels'''
        
        return Guilds.private_channels
    
    Listener.subscribe_event('READY', __set_guilds)
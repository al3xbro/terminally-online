import json
import sys
from websocket.listener import Listener

class Guilds:
    
    guilds = {}
    private_channels = []

    guilds_dirview = {}

    @staticmethod
    def __set_guilds(data: dict) -> None:
        '''Set the guilds'''

        Guilds.guilds = data['guilds']
        Guilds.private_channels = data['private_channels']

        for guild in Guilds.guilds:
            
            # create guild
            Guilds.guilds_dirview[guild['id']] = {
                'name': guild['name'],
                'categories': []
            }

            # add categories
            for channel in guild['channels']:
                if channel['type'] == 4:
                    Guilds.guilds_dirview[guild['id']]['categories'].append({
                        'id': channel['id'],
                        'name': channel['name'],
                        'position': channel['position'],
                        'channels': []
                    })

            # add channels to categories
            for channel in guild['channels']:
                if channel['type'] == 0:
                    min_category = None

                    # find the category it belongs to
                    for category in Guilds.guilds_dirview[guild['id']]['categories']:
                        if min_category is None:
                            min_category = category
                        elif channel['position'] > category['position'] and category['position'] < min_category['position']:
                            min_category = category

                    # add channel if it is uncategorized
                    if min_category:
                        min_category['channels'].append({
                            'id': channel['id'],
                            'name': channel['name'],
                            'position': channel['position']
                        })
                    # if no category, that means it's uncategorized
                    else:
                        # if there no an uncategorized, make one
                        if len(Guilds.guilds_dirview[guild['id']]['categories']) == 0 or Guilds.guilds_dirview[guild['id']]['categories'][0]['name'] != 'uncategorized':
                            Guilds.guilds_dirview[guild['id']]['categories'].insert(0, {
                                'id': 0,
                                'name': 'uncategorized',
                                'position': -1,
                                'channels': [{
                                    'name': channel['name'],
                                    'position': channel['position']
                                }]
                            })
                        # add channel to uncategorized
                        else:
                            Guilds.guilds_dirview[guild['id']]['categories'][0].append({
                                'id': channel['id'],
                                'name': channel['name'],
                                'position': channel['position']
                            })

        json.dump(Guilds.guilds_dirview, open('bruh', 'w'))
    
    @staticmethod
    def get_guilds() -> list:
        '''Returns the guilds'''
        
        return Guilds.guilds
    
    @staticmethod
    def get_private_channels() -> list:
        '''Returns the private channels'''
        
        return Guilds.private_channels
    
    Listener.subscribe_event('READY', __set_guilds)
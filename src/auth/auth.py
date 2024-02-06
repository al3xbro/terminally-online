import requests
import json
import os
from enum import Enum

CONFIG_PATH = os.path.abspath(os.path.expanduser('~/.config/termon/'))
TOKEN_PATH = os.path.join(CONFIG_PATH, 'token')

class LoginStatus(Enum):
    SUCCESS = 'success'
    NEED_MFA = 'need_mfa'
    FAILED_VERIFICATION_EMAIL = 'failed_verification_email'
    FAILED_CREDENTIALS = 'failed_login'
    FAILED_MFA = 'failed_mfa'
    INVALID_TOKEN = 'invalid_token'

class LogoutStatus(Enum):
    SUCCESS = 'success'
    FAILED = 'failed'

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

def login(email: str, password: str, mfa_code: str = None) -> LoginStatus:
    '''Saves login token and returns a LoginStatus'''

    # send login request
    res = requests.post(url = 'https://discord.com/api/v9/auth/login', 
                        data = json.dumps({
                            'gift_code_sku_id': None,
                            'login': email,
                            'password': password,
                            'login_source': None,
                            'undelete': False,
                        }), 
                        headers = headers | {'referer': 'https://discord.com/login'})

    # verify ip
    if res.json().get('errors') and res.json().get('errors').get('login').get('_errors')[0].get('code') == 'ACCOUNT_LOGIN_VERIFICATION_EMAIL':
        return LoginStatus.FAILED_VERIFICATION_EMAIL
    
    # invalid credentials
    if res.json().get('errors') and res.json().get('errors').get('login').get('_errors')[0].get('code') == 'INVALID_LOGIN':
        return LoginStatus.FAILED_CREDENTIALS
    
    # need MFA code
    if res.json().get('ticket') and mfa_code is None:
        return LoginStatus.NEED_MFA
    
    # make the MFA request
    if res.json().get('ticket') and mfa_code is not None:
        res = requests.post(url = 'https://discord.com/api/v9/auth/mfa/totp', 
                            data = json.dumps({
                                'code': mfa_code,
                                'ticket': res.json().get('ticket'),
                            }), 
                            headers = headers | {'referer': 'https://discord.com/login'})
        
        # invalid MFA code
        if res.json().get('code') == 60008:
            return LoginStatus.FAILED_MFA
        
    # successful login
    os.makedirs(CONFIG_PATH, exist_ok=True)
    with open(TOKEN_PATH, 'w+') as f:
        f.write(res.json().get('token'))
    return LoginStatus.SUCCESS

def logout() -> LogoutStatus:
    '''Invalidates login token and returns a LogoutStatus'''

    # send logout request
    res = requests.post(url = 'https://discord.com/api/v9/auth/logout', 
                        headers = headers | {
                            'referer': 'https://discord.com/login', 
                            'authorization': get_token(),
                        },
                        data = json.dumps({
                            'provider': None,
                            'voip_provider': None,
                        }))
    
    if res.status_code == 204:
        return LogoutStatus.SUCCESS
    return LogoutStatus.FAILED

def get_token() -> str:
    '''Returns the login token'''
    with open(TOKEN_PATH, 'r') as f:
        return f.read()
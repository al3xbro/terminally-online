import requests
import json
from enum import Enum

# TODO: STORING TOKEN IN JSON FOR NOW. CHANGE LATER

class LoginStatus(Enum):
    SUCCESS = 'success'
    NEED_MFA = 'need_mfa'
    FAILED_VERIFICATION_EMAIL = 'failed_verification_email'
    FAILED_CREDENTIALS = 'failed_login'
    FAILED_MFA = 'failed_mfa'

# base headers for all requests. add referer and authorization
f = open('base_headers.json', 'r')
headers = json.load(f)
f.close()

# Saves login token and returns a LoginStatus
# param: email, password, mfa_code?
# return: LoginStatus
def login(email: str, password: str, mfa_code: str = None):

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
        # successful login with MFA
        with open('token.json', 'w') as f:
            json.dump({'token': res.json().get('token')}, f)
        return LoginStatus.SUCCESS
    # successful login without MFA
    with open('token.json', 'w') as f:
        json.dump({'token': res.json().get('token')}, f)
    return LoginStatus.SUCCESS

def logout():

    # send logout request
    res = requests.post(url = 'https://discord.com/api/v9/auth/logout', 
                        headers = headers | {'referer': 'https://discord.com/login', 'authorization': ''})


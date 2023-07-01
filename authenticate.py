import tableauserverclient as TSC
from tableau_api_lib import TableauServerConnection
from config import *

# Sign in and auth with token

config = {
    'tableau_server': {
        'server': server_url,
        'api_version': '3.15', # whatever version your Tableau Server uses
        'personal_access_token_name': token_name,
        'personal_access_token_secret': token_secret,
        'site_name': site_name,
        'site_url': site_url
    }
}

conn = TableauServerConnection(config, env="tableau_server")

def tableau_sign_in():
    print(f'Sign in HTTP status: {conn.sign_in().status_code}')

def tableau_sign_out():
    print(f'Sign Out HTTP status {conn.sign_out().status_code}')
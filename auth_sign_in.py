import tableauserverclient as TSC
from tableau_api_lib import TableauServerConnection
from var import *

# Sign in and auth with token

config = {
    'tableau_server': {
        'server': server_string,
        'api_version': '', # whatever version your Tableau Server uses
        'personal_access_token_name': token_name,
        'personal_access_token_secret': token_secret,
        'site_name': site_name,
        'site_url': site_url
    }
}

conn = TableauServerConnection(config, env="tableau_server")

def tableau_sign_in():
    conn.sign_in()
    print(f'Sign in Response Code: {conn.sign_in()}')

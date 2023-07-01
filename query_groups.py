# Dependencies
from authenticate import *
import json

# Sign in with server_auth
tableau_sign_in()


def group_json(data):
    '''Selectively grabbing name and id from raw json. 
    This is being used in get_group()'''
    name = data['name']
    group_id = data['id']
    site_role = data.get('import', {}).get('siteRole')
    return {'name': name, 'id': group_id, 'site_role': site_role}


def get_group():
    '''Return a list of names and ids for all the existing groups'''
    response = conn.query_groups()
    print(f'Query group HTTP status: {response.status_code}')
    group_data = response.json()['groups']['group']
    group_list = list(map(group_json, group_data))
    print(f'Here are the groups in {site_name} site:')
    print(json.dumps(group_list, indent=2)) 
    return group_list

# Uncomment to try it out!
# get_group()
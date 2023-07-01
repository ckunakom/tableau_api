# Dependencies
from query_groups import *

###############################################################
'''This file is for creating groups when a new site has been 
    added to the server.'''
###############################################################

# TODO: Create Groups  
'''Manually define what the group name and the minimum 
    site role should be.'''

group_obj = [
    {'group_name': 'Test0', 'min_site_role': None},
    {'group_name': 'Test1', 'min_site_role': 'Creator'},
    {'group_name': 'Test2', 'min_site_role': 'Explorer'},
    {'group_name': 'Test3', 'min_site_role': 'Viewer'}
]

# Query existing group
existing_group = get_group()

# Create group
group_name_list = [e['name'] for e in existing_group]

print('Creating groups...')
for g in group_obj:
    if g['group_name'] not in group_name_list:
        response = conn.create_group(new_group_name=g['group_name'], minimum_site_role=g['min_site_role'])
        print(f"Created Group: {g['group_name']}, Status - {response.status_code}")
    else:
        print(f"{g['group_name']} already exists.")

# Sign out of Tableau
tableau_sign_out()

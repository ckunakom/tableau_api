# Dependencies
from query_groups import *
from variables import *
###############################################################
'''This file is for creating groups when a new site has been 
    added to the server.'''
###############################################################

# Query existing group
existing_group = get_group()

# Create group
group_name_list = [e['name'] for e in existing_group]
print('Creating groups...')

# See `variables.py` for the defined `group_obj`
for g in group_obj:
    if g['group_name'] not in group_name_list:
        response = conn.create_group(new_group_name=g['group_name'], minimum_site_role=g['min_site_role'])
        print(f"Created Group: {g['group_name']}, Status - {response.status_code}")
    else:
        print(f"{g['group_name']} already exists.")

# Sign out of Tableau
tableau_sign_out()

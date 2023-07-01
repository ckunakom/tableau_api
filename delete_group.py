# Dependencies
from tableau_api_lib.utils import querying
from authenticate import *

# Sign in with auth_sign_in
tableau_sign_in()

# ###############################################################
# '''This file is for deleting groups with user's 
#     selection as input'''
# ###############################################################

# Prompt user to make selection
prompt = input('Would you like to delete an existing group? (Y/N): ').upper()

# List out and show the user the list of groups
def list_group():
    group_df = querying.get_groups_dataframe(conn)
    group_list = group_df['name']
    print(f'Here are all the groups in {site_name} site:')
    print(group_list)

    return group_df, group_list

# Prompt user to select group based on #
while prompt == 'Y':
    
    # Get the returned vars from the list_group()
    group_df, group_list = list_group()

    # Assign the variable group name
    select_group = int(input('Select the # corresponds to the group you want to delete: '))
    group_name = group_list[select_group]

    # Get the group id from user's selection
    group_id = group_df['id'][group_df['name'] == group_name].values[0]

    # Delete selected group
    response = conn.delete_group(group_id)
    print(f'Deleted group {group_name} HTTP status: {response.status_code}')

    prompt = input('Would you like to delete another existing group? (Y/N): ').upper()
    
print(f'We are done here.')

# Sign out of the server
tableau_sign_out()
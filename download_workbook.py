from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import querying, flatten_dict_column
from auth_sign_in import *
import os

# Sign in with auth_sign_in
tableau_sign_in()

###############################################################

# Query the project and show the user the list of projects
projects_df = querying.get_projects_dataframe(conn)
project_list = projects_df['name']
print(project_list)

# Assign the variable with project name
select_project = int(input('Select the # corresponds to the project you want: '))
project_name = project_list[select_project]

###############################################################

# Query workbook in dataframe
workbooks_df = querying.get_workbooks_dataframe(conn)

# Flatten the project object in data frame to get id and name
workbook_df = flatten_dict_column(df=workbooks_df, keys=['id', 'name'], col_name='project')

# Zero in for items in that project 
target_project_df = (
    workbook_df
    .where(workbook_df['project_name'] == project_name) 
    .dropna()
)

###############################################################

print(f'----Input selection: {project_name}----')
print('Here are all the workbooks in this project')
print(target_project_df['name'])

###############################################################

# Create a list of workbooks we want to download
selected_wkbk_list = []
# Turned the `target_project_df['name']` to list for selection
workbook_list = target_project_df['name'].tolist()

# Infinitely appending the list until the loop breaks
while True:

    try:
        # Prompt for user
        # Turn the input to int for index
        user_input = int(input('Select the # of workbook: '))
        selected_index = target_project_df['name'][user_input]
        
        # Add item in the list if it exists
        if selected_index in workbook_list:
            # Don't add the same iteam in the list
            if  selected_index in selected_wkbk_list:
                continue
            else:
                # Append list with wkbk
                selected_wkbk_list.append(selected_index)
                print(f'Confirmed: "{selected_index}" entered')
                print('----------------------------------------------------------------------------------')
                print("Input string or press enter to move on if you don't have any more workbook to enter")
        else:
            break

    except KeyError:
        print("----Selection does not exist. Try again----")
    
    except:
        print('Selection Comlete')
        break

# Print out what we have at the end   
print('----Workbook(s) selected----')
print(selected_wkbk_list)

print('**********************************************************************')
print('--------------------Workbook Downloading Time!------------------------')
print('**********************************************************************')

for wkbk in selected_wkbk_list:

    # Store the workbook_id of the workbook we want
    workbook_id = target_project_df[target_project_df['name'] == wkbk]['id'].values[0]
    print(f'----Grabbed id for {wkbk}----')

    # Download the workbook content -- tableau api method in action
    download_wkbk_response = conn.download_workbook(
        workbook_id=workbook_id
    )

    ###############################################################
    ########## Organize the workbook in their own folders #########
    ###############################################################

    # Remove white space (if any) at the end of the workbook name (you never know!)
    wkbk_name = wkbk.rstrip()

    # Check to see if path exist
    is_exist = os.path.exists(wkbk_name)

    if not is_exist:        
        # create a new directory
        os.makedirs(wkbk_name)
        print(f'Confirmed: {wkbk_name} directory created')
        print('----------------------------------------------------------------------')
        
        try:
            # Created the file here with that path
            # Write the content to twb file
            open(f'{wkbk_name}/{wkbk_name}.twb', 'wb').write(download_wkbk_response.content)
            print(f'Confirmed: {wkbk_name} downloaded and placed in {wkbk_name} directory')
            print('----------------------------------------------------------------------')
        except FileNotFoundError:
            print(f'Confirmed: {wkbk_name} directory is not found')
            print('----------------------------------------------------------------------')

    else:
        print(f'Confirmed: {wkbk_name} directory already exists.')
        print('----------------------------------------------------------------------')

        try:
            # Created the file here with that path
            open(f'{wkbk_name}/{wkbk_name}.twb', 'wb').write(download_wkbk_response.content)
            print(f'Confirmed: {wkbk_name} downloaded and placed in {wkbk_name} directory')
            print('----------------------------------------------------------------------')
        except FileNotFoundError:
            print(f'Confirmed: {wkbk_name} directory is not found')
            print('----------------------------------------------------------------------')

print(f'Done!')

# Sign out of the server
conn.sign_out()
print('----Signed out----')
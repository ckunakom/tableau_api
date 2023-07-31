# Dependencies
import time
from tableau_api_lib.utils import querying
from all_user_none_permission import *

###############################################################
'''This file is for creating projects when a new site has been
    added to the server and the project structure needs to mimic
    the existing structure as the other site.'''
###############################################################

# TODO: List out name of projects to be created create
projects = ['Test']

# Get the group id for All Users
all_user = get_all_users_id()

# List of existing projects in the site
project_df = querying.get_projects_dataframe(conn)
exist_project = project_df['name'][project_df['parentProjectId'].isnull()].tolist()

for p in projects:
    # Create the project if doesn't exist as Parent project
    if p not in exist_project:
        response = conn.create_project(project_name=p)
        print(f'Project Created: {p} - Status {response.status_code}')
    # Let's think more about this one
    else:
        print(f'{p} already exists.')

    # Get newly created project Id
    time.sleep(3)
    new_project_df = querying.get_projects_dataframe(conn)
    project_id = new_project_df[(new_project_df['name'] == p) & (new_project_df['parentProjectId'].isnull())]['id'].values[0]

    #### Remove default permission for `All User` ####
    #### ---------------------------------------- ####
    # Generic prrmission to remove
    standard_capability = ['Write', 'Read']

    # Remove permission for Project, Flow, Data Roles, Lens and Metrics
    project_remove_group_perm(project_id, all_user, standard_capability)
    other_remove_group_default_perm(project_id, all_user, standard_capability)

    # Remove permission for workbooks, datasource
    workbook_remove_group_default_perm(project_id, all_user)
    datasource_remove_group_default_perm(project_id, all_user)

# Should theses be a function or another file? 

    #### Creating child projects with carried over permission configuration of all the groups ####
    #### ------------------------------------------------------------------------------------ ####

    #1. Add all the groups and config perm -- note to self: this needs to be part of create_projects
    # Objects with different capability permission to configure
    # TODO: Update as needed
    perm_allow = {'Read': 'Allow', 'Write': 'Allow'}
    perm_deny = {'Read': 'Deny', 'Write': 'Deny'}
    perm_explore = {'Read': 'Allow', 'Write': 'Deny'}

    # Groups to be configured with permission
    creator_group = ['Test1']
    explorer_group = ['Test2', 'Test3']
    deny_group = ['Test0']

    # TODO: In progress
    # # Add permission for the above
    # for x in perm_add:
    #     response = conn.add_project_permissions(project_id=project_id, group_capability_dict=x['permission'], group_id=x['id'])
    #     print(response.status_code)
    
    #2. Create sub-project with inherited configured permission
    ''' This will automatically add the user who runs the api code as the 
        Project Leader for these sub-projects. To remove, see #3 or comment out.'''
    # TODO: Create list of sub-projects
    sub_projects = ['Sub-Test1', 'Sub-Test2']

    for s in sub_projects:
        response = conn.create_project(project_name=f'{p} {s}', parent_project_id=project_id)
        print(f'Sub-project {s} Created in {p} HTTP Status: {response.status_code}')

    #3. Removed InheritedProjectLeader from the User running the code
    # TODO: Input your Tableau Server Username
    username_input = input('Enter your username: ')
    user_df = querying.get_users_dataframe(conn)
    target_user_id = user_df[user_df['name'] == username_input]['id'].values[0]
    print(f'User ID to be stripped off InheritedProjectLeader capability: {target_user_id}')

    #4. Get id of the sub-project to remove the ProjectLeader
    sub_df = querying.get_projects_dataframe(conn)
    sub_project_list = sub_df[sub_df['parentProjectId'] == project_id]['id'].tolist()
    print(f'List of Sub-project ID: {sub_project_list}')

    # Remove 'ProjectLeader' capability from subprojects
    for s in sub_project_list:
        delete_response = conn.delete_project_permission(
            project_id=s,
            capability_name='InheritedProjectLeader',
            capability_mode='Allow',
            delete_permissions_object='users',
            delete_permissions_object_id=target_user_id,
        )
        print(f'Removed Project Leader Capability from user ID {target_user_id} on Sub-project {s} HTTP Status: {delete_response.status_code}')

# Sign out of Tableau
tableau_sign_out()


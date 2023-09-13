# Dependencies
import time
from tableau_api_lib.utils import querying
from remove_permission_util import *
# Correspond the variables used in this file with `variables.py`, indicated with 'Section'
from variables import *

###############################################################
'''This file is for creating projects when a new site has been
    added to the server and the project structure needs to mimic
    the existing structure as the other site.'''
###############################################################

# Get the group id for All Users
all_user = get_all_users_id()[1]

# List of existing projects in the site
project_df = querying.get_projects_dataframe(conn)
exist_project = project_df['name'][project_df['parentProjectId'].isnull()].tolist()

# Variable Section A
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

    #### Creating child projects with carried over permission configuration of all the groups ####
    #### ------------------------------------------------------------------------------------ ####

    #1. Add all the groups and config perm 
    # Get all the groups existing in the site
    all_groups = get_all_users_id()[0]

    # Add permission for the groups as defined earlier
    # TODO: Add permission method for other object as needed
    for a in all_groups:
        print(f"HTTP Status for configuring permission of {a['name']} Group:")
        
        # Variable Section B
        if a['name'] in admin_group:
            '''Admin already has a default permission for all objests, so no need to configure other objects.'''
            project_response = conn.add_project_permissions(
                project_id=project_id, 
                group_capability_dict=perm_admin, 
                group_id=a['id']
            )

        elif a['name'] in creator_group:
            project_response = conn.add_project_permissions(
                project_id=project_id, 
                group_capability_dict=perm_allow, 
                group_id=a['id'])

            data_response = conn.add_default_permissions(
                project_id=project_id,
                project_permissions_object='datasource',
                group_capability_dict=ds_perm_allow,
                group_id=a['id'],
            )
            wkbk_response = conn.add_default_permissions(
                project_id=project_id,
                project_permissions_object='workbook',
                group_capability_dict=wkbk_perm_allow,
                group_id=a['id'],
            )

        elif a['name'] in explorer_group:
            project_response = conn.add_project_permissions(
                project_id=project_id, 
                group_capability_dict=perm_explore, 
                group_id=a['id'])

            data_response = conn.add_default_permissions(
                project_id=project_id,
                project_permissions_object='datasource',
                group_capability_dict=ds_perm_explore,
                group_id=a['id'],
            )
                                
            wkbk_response = conn.add_default_permissions(
                project_id=project_id,
                project_permissions_object='workbook',
                group_capability_dict=wkbk_perm_explore,
                group_id=a['id'],
            )

        elif a['name'] in deny_group:
            project_response = conn.add_project_permissions(
                project_id=project_id, 
                group_capability_dict=perm_deny, 
                group_id=a['id'])

            data_response = conn.add_default_permissions(
                    project_id=project_id,
                    project_permissions_object='datasource',
                    group_capability_dict=ds_perm_deny,
                    group_id=a['id'],
            )
                                
            wkbk_response = conn.add_default_permissions(
                    project_id=project_id,
                    project_permissions_object='workbook',
                    group_capability_dict=wkbk_perm_deny,
                    group_id=a['id'],
            )

        else:
            print(f'No permission has been configured.')
        
        try:
            print(f'Project permission: {project_response.status_code}')
            print(f'Data Source permission: {data_response.status_code}')
            print(f'Workbook permission: {wkbk_response.status_code}')

        except NameError:
            continue

    #2. Create sub-project with inherited configured permission
    ''' This will automatically add the user who runs the api code as the 
        Project Leader for these sub-projects. To remove, see #3 or comment out.'''

    # Variable Section C
    for s in sub_projects:
        response = conn.create_project(project_name=s, parent_project_id=project_id)
        print(f'Sub-project {s} Created in {p} HTTP Status: {response.status_code}')

    #3. Removed InheritedProjectLeader from the User running the code
    user_df = querying.get_users_dataframe(conn)
    # Variable Section D
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


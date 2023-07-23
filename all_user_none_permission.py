# Dependencies
from query_groups import *

def get_all_users_id():
    '''Get the group id of All User.'''
    group_list = get_group()
    all_users_id = next((g['id'] for g in group_list if g['name'] == 'All Users'), None)
    print(f'Id for All Users Group: {all_users_id}')
    return all_users_id

# Default Capability for Project, Flow, Data Roles, Lens and Metrics
perm_capability = ['Write', 'Read']

def project_remove_group_perm(project_id, group_id, perm_capability):
    '''Remove previously configured Read & Write permission to a group for a project.
        When using Tableau Rest API to create projects, the All Users group
        will be automatically configured to have both Write and Read permission allowed.
        Remove the permission to give All Users a None permission configuration with 
        this function.'''
    for p in perm_capability:
        response = conn.delete_project_permission(
            project_id=project_id,
            delete_permissions_object="groups",
            delete_permissions_object_id=group_id,
            capability_name=p,
            capability_mode="Allow",
        )
        print(f'Removed {p} capabililty from group id {group_id} HTTP status: {response.status_code}')



def other_remove_group_default_perm(project_id, group_id, perm_capability):
    default_perm_obj = ["flows", "dataroles", "lenses", "metrics"]
    
    for p in perm_capability:
    
        for d in default_perm_obj:
            response = conn.delete_default_permission(
                project_id=project_id,
                project_permissions_object=d,
                delete_permissions_object="group",
                delete_permissions_object_id=group_id,
                capability_name=p,
                capability_mode="Allow",
            )
        print(f'Removed {p} capabililty for {d} from group id {group_id} HTTP status: {response.status_code}')
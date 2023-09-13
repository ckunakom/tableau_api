# TODO: Update as needed
''' Define all the variables and their TODO here to unclutter '''

# Used in create_group.py 
# Manually define what the group name and the minimum site role should be.
group_obj = [
    {'group_name': 'Test0', 'min_site_role': None},
    {'group_name': 'Test1', 'min_site_role': 'Creator'},
    {'group_name': 'Test2', 'min_site_role': 'Explorer'},
    {'group_name': 'Test3', 'min_site_role': 'Viewer'}
]

# Section A: List out name of projects to be created create
projects = ['Test']

# Section B: Groups to be configured with permission
admin_group = ['Admin_Test']
creator_group = ['Test1']
explorer_group = ['Test2', 'Test3']
deny_group = ['Test0']

#  Objects with different capability permission to configure
# Project Capability Template
perm_admin = {'ProjectLeader': 'Allow'}
perm_allow = {'Read': 'Allow', 'Write': 'Allow'}
perm_deny = {'Read': 'Deny', 'Write': 'Deny'}
perm_explore = {'Read': 'Allow', 'Write': 'Deny'}

# Data source Capability Template
ds_perm_allow = {
    'Read': 'Allow',
    'ExportXml': 'Allow',
    'Connect': 'Allow',
    'Write': 'Allow',
    'SaveAs': 'Allow',
}
ds_perm_deny = {'Read': 'Deny', 'ExportXml': 'Deny', 'Connect': 'Deny'}
ds_perm_explore = {'Read': 'Allow', 'ExportXml': 'Allow', 'Connect': 'Allow'}

# Workbook Capability 
# Define them according to your needs
wkbk_perm_allow = {}
wkbk_perm_deny = {}
wkbk_perm_explore = {}

# Define the other object capabilities to configure
''' flow_perm_<allow/deny/explore> = {}
    metric_perm_<allow/deny/explore> = {}
    dataroles_perm_<allow/deny/explore> = {} 
    lenses_perm_<allow/deny/explore> = {}
    metrics_perm_<allow/deny/explore> = {}
'''

# Section C: Create list of sub-projects
sub_projects = ['Sub-Test1', 'Sub-Test2']

# Section D: Input your Tableau Server Username to remove InheritedProjectLeader
print('Enter your Tableau Server username: ')
username_input = input()
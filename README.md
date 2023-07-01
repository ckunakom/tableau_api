# Create more functionality in Tableau Server with Rest API
Tableau Server REST API Doc: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm

Here is some of the usage that I tried out and put to use:
- Download Workbooks for Git Revision
- Create Groups, Projects and Set Permission for each group for the Project

### Before Running Files
Create python virtual environment and `pip install` the following modules:
- TableauServerConnection
- requests
- tableau_api_lib
- python-dotenv

Fill out `env.txt` with your API token and Tableau Server information and rename it to `.env`.

Here's where you can create a Personal Access Token: https://help.tableau.com/current/online/en-us/security_personal_access_tokens.htm  

### Download Workbooks for Git Revision
Quick shout-out to this youtube video as it saves me the trouble of some readings🤫: https://youtu.be/swasTFYM_Gs

One of the capabilities that Tableau Server does not offer is integration with Git. You can view the previous revisions with Tableau Server, but only up to certain number of revisions (I think it's up to 20? 25?). As someone who used to work in Audit and Monitoring department, that was heart-breaking. However, not all hope is lost since there is a an effective way of downloading the workbooks without using the UI, which involves lot of multiple mouse-clicking.

Use/Run the `download_workbook.py` and follow the prompt. It's interactive!
- User will select some numbers corresponding to the project and the workbooks they need to download
- Once the selection is complete, the workbooks will be downloaded and place in a directory which gets created with the same name of the workbook (if one doesn't already exist).
- The files are ready to be added, committed and push to the repo. 

### Create Groups, Projects and Set Permission for each group for the Project
This is particularly useful when you have different Tableau Sites or Servers that you need to configure the same group permission with the projects. Save you a lot of mouse-clicking.
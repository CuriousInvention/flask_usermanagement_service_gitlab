from dotenv import load_dotenv
import requests
import os


class GitlabConfigService:
    def __init__(self, gitlab):
        self.gitlab = gitlab
        
    def get_access_token(self):
        token = self.gitlab.authorize_access_token()
        
        access_token = token.get('access_token')
        
        if not access_token:
            return "Error: No access token provided.", 400
        print("Access toekn :: ",access_token)
        return access_token
    
    def get_user_details(self, access_token):
        # Make a request to GitLab API to get the user details
        user_info_url = os.getenv('GITLAB_CONFIG_USER_URI')
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code != 200:
            return f"Error fetching user details: {response.status_code}", 400

        user = response.json()
        print('user :: ',user)
            
        return user

    def get_usergroup_details(self, access_token):
        # Make a request to GitLab API to get the user details
        group_info_url = "https://gitlab-dev.stackroute.in/api/v4/groups?per_page=999"

        # Set up the headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(group_info_url, headers=headers)

        if response.status_code != 200:
            return f"Error fetching user details: {response.status_code}", 400

        # Extract group name from groups data
        extract_group_name = GitlabConfigService.extract_group_names(response.json())
            
        #  Based on group assign role
        return GitlabConfigService.check_group_type(extract_group_name)

    def extract_group_names(groups):
        """
        Extracts the 'name' from a list of group dictionaries.

        :param groups: List of dictionaries where each dictionary represents a group.
        :return: List of group names.
        """
        return [group.get('name') for group in groups]

    def check_group_type(group_list):
        """
        Checks the group list for 'admin' or 'master' and returns the appropriate role.

        :param group_list: List of group names.
        :return: 'admin' if 'admin' or 'master' is found, otherwise 'learner'.
        """
        if 'genai_admin' in group_list:
            return 'ADMIN'
        elif 'genai_master' in group_list:
            return 'MASTER'
        else:
            return 'LEARNER'
        
     
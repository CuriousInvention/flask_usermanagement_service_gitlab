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

        
     
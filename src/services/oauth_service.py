# from utils.gitlab.gitlab_config_service import GitlabConfigService 
from model.user import User

class OAuthService:
    # Code here
    def __init__(self):
        self.users = {}
        
    def xyz():
        return "some"
    
    def save_user(self, user: User):
        if user.username in self.users:
            raise ValueError("Username already exists.")
        if any(u.email == user.email for u in self.users.values()):
            raise ValueError("Email already exists.")
        self.users[user.username] = user
        # self.users[user.username] = user
        # self.users[user.username] = user
        # self.users[user.username] = user
        # self.users[user.username] = user
        print(f"User {user.username} saved successfully.")
        return user
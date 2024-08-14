from flask import Blueprint, jsonify, Flask, make_response, redirect, url_for, session, request
from utils.gitlab.gitlab_config_service import GitlabConfigService 
from utils.jwt.jwt_config_service import JwtConfigService
from authlib.integrations.flask_client import OAuth
from services.oauth_service import OAuthService
from model.user import User
import secrets
import os


oauth_bp = Blueprint('oauth_bp','__name__')
flaskapp = Flask(__name__)
oauth = OAuth(flaskapp)

gitlab = oauth.register(
    name = os.getenv('GITLAB_CONFIG_APP_NAME'),
    client_id = os.getenv('GITLAB_CONFIG_CLIENT_ID'),
    client_secret = os.getenv('GITLAB_CONFIG_CLIENT_SECRET'),          
    authorize_url = os.getenv('GITLAB_CONFIG_AUTHORIZE_URL'),          
    access_token_url = os.getenv('GITLAB_CONFIG_ACCESS_TOKEN_URI'),          
    redirect_uri = os.getenv('GITLAB_CONFIG_CALLBACK_REDIRECT_URI'),     
    client_kwargs =  {'scope': 'api read_user'} #os.getenv('GITLAB_CONFIG_CLIENT_KWARGS')
)

# Service initialization
gitlab_service = GitlabConfigService(gitlab)

# Health Check End-Point
@oauth_bp.route("/health", methods=["GET"])
def health_check():
    return "Service is working ok", 200


# Login
@oauth_bp.route("/")
def login():
    # ------------------
    # Check if user already login, 
    # if login then redirect to home page
    # else do the login process
    # ------------------
    
    user = session.get('user')
    
    if user:
        # return redirect(os.getenv('REDIRECT_ROUTE'))
        return user
    
    # login process
    nonce = secrets.token_urlsafe()
    session['nonce'] = nonce
    
    redirect_uri = url_for('oauth_bp.auth_callback', _external=True)
    return gitlab.authorize_redirect(redirect_uri, nonce=nonce)
 

@oauth_bp.route('/oauth/callback')
def auth_callback():
    print("\n-------> Auth Callback <------")
    access_token = gitlab_service.get_access_token()
    user_detail = gitlab_service.get_user_details(access_token)
    # user_group = gitlab_service.get_user_details(access_token)
    
    
    
    print('user_detail :: ',user_detail)
    
    # IF user avail then >> update
    
     # Create a new user
    new_user = User(
        username=user_detail['email'],
        email=user_detail['email'],
        name=user_detail['name'],
        role= "MASTER",
        status="ENABLED",
        createdBy="gitlab"
    )
    
    # Saving user to db
    oauthservice = OAuthService()
    saved_user = oauthservice.save_user(new_user)
    
    
    # Generating Jwt token
    user_info_for_token = {
        "username" : user_detail['email'],
        "email" : user_detail['email'],
        "name" : user_detail['name'],
        "role" :  "MASTER",
        "status" : "ENABLED",
        "createdBy" :"gitlab"
    }
    
    jwt_token = JwtConfigService.generate_jwt_token(user_info_for_token)
    print('>>token >>> ',jwt_token);
    
    session['user'] = saved_user
    
    # Set the cookie with appropriate options (secure, HttpOnly, etc.)
    response = jsonify({'user' : saved_user, 'message': 'Login successful'})
    response.set_cookie('cookies', jwt_token, secure=True, httponly=True)
    return redirect(os.getenv('REDIRECT_ROUTE'))
    # return response
    
    

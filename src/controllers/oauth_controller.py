from flask import Blueprint, jsonify, Flask, redirect, url_for, session, request
from utils.gitlab.gitlab_config_service import GitlabConfigService 
from utils.jwt.jwt_config_service import JwtConfigService
from authlib.integrations.flask_client import OAuth
from services.oauth_service import OAuthService
from model.user import User
import secrets
import os
from flask import make_response


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
    client_kwargs =  {'scope': 'api read_user'}
)

# Service initialization
gitlab_service = GitlabConfigService(gitlab)
oauth_service = OAuthService()

# Health Check End-Point
@oauth_bp.route("/health", methods=["GET"])
def health_check():
    return "Service is working ok", 200


# Login
@oauth_bp.route("/")
def login():
    
    # temp check will remove later once stable
    # user = session.get('user')
    cookies = request.cookies

    if cookies:
        # If cookies are available, print the values
        for key, value in cookies.items():
            print(f"Cookie '{key}' has value: {value}")
        
        response = make_response(redirect(os.getenv('REDIRECT_ROUTE')))
        return response
    
    # login process
    nonce = secrets.token_urlsafe()
    # session['nonce'] = nonce
    
    redirect_uri = url_for('oauth_bp.auth_callback', _external=True)
    return gitlab.authorize_redirect(redirect_uri, nonce=nonce)
 

@oauth_bp.route('/oauth/callback')
def auth_callback():
    access_token = gitlab_service.get_access_token()
    user_detail = gitlab_service.get_user_details(access_token)

    check_group_and_get_role = gitlab_service.get_usergroup_details(access_token)

    # prepare data
    user = {
        "username": user_detail['email'],
        "email": user_detail['email'],
        "name": user_detail['name'],
        "role": check_group_and_get_role,
        "status": user_detail['state']
    }

    # Saving user to mongodb (user_db >> users)
    # oauth_service = OAuthService()

    reterive_user = oauth_service.retrieve_user(user['email'])

    saved_user_detail = {}
    
    if reterive_user is None: 
        user["createdBy"] = user['email']
        user["updatedBy"] = user['email']
        user["origin"] = "Gitlab-dev"

        print('saving user deatil : ',user)
        saved_user_detail = oauth_service.save_user(user)
    else:
        user["updatedBy"] = user['email']
        print('updating user deatil : ',user)
        saved_user_detail = oauth_service.update_user(user['email'], user)

    
    # Token generation
    jwt_token = JwtConfigService.generate_jwt_token(user)
    
    # session['user'] = user
    response = make_response(redirect(os.getenv('REDIRECT_ROUTE')))

    # response.set_cookie('auth_token', jwt_token, httponly=True, secure=True, samesite='Lax')
    # response.set_cookie('cookies', jwt_token, httponly=True, samesite='Lax')
    # response.set_cookie('cookies', jwt_token, httponly=True, samesite='Lax', domain='localhost')
    response.set_cookie('cookies', jwt_token)

    return response
    
    
@oauth_bp.route('/get_user')
def get_user():
    # Retrieve the 'email' parameter from the query string
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    # oauth_service = OAuthService()

    user = oauth_service.retrieve_user(email)
    print('reterived user using Email :: ',user)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@oauth_bp.route('/load_user')
def load_user():
    auth_cookies = request.cookies.get()
    print('auth cookies :: ',auth_cookies)

    if(auth_cookies):
        parse_token = JwtConfigService.parse_token(auth_cookies)
    # oauth_service = OAuthService()
        user_info = oauth_service.retrieve_user(parse_token['email'])
        return user_info
    else:
        return "Token expired, Invalid"

    
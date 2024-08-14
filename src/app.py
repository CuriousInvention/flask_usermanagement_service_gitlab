from flask import Flask
from flask_cors import CORS
import os
from controllers.oauth_controller import oauth_bp
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
# from services.oauth_service import OAuthService


app = Flask(__name__)
CORS(app)
# oauth = OAuth(app)
# app.oauth = OAuth(app)
app.secret_key = os.getenv('SECRET_KEY')
# Set JWT token location to cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Other desired JWT configurations (optional)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # Enable CSRF protection

# Initialize JWT manager
jwt = JWTManager(app)


app.register_blueprint(oauth_bp)

if __name__ == '__main__':
    print('Python flask server started....')
    # print("os.env :: ",os.getenv('GITLAB_CONFIG_NAME'))
    # print('OauthService ::: ', OAuthService.xyz())
    
    # Create a new user
    # new_user = User(
    #     username="john_doe",
    #     email="john@example.com",
    #     name="John Doe",
    #     role=Role.LEARNER,
    #     status=Status.ENABLED,
    #     createdBy="admin_user"
    # )
    
    # oauthservice = OAuthService()
    # oauthservice.save_user(new_user)
    
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
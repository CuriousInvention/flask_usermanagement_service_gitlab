from flask import Flask
from flask_cors import CORS
import os
from controllers.oauth_controller import oauth_bp
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
# from services.oauth_service import OAuthService


app = Flask(__name__)
CORS(app)
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
    
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
import jwt
import datetime
import os


SECRET_KEY = 'random_secret_key'

class JwtConfigService:   
    def generate_jwt_token(user_info):
 
        payload = {
            'name' : user_info['name'],
            'email' : user_info['email'],
            'role' : user_info['role'],
            'status' : user_info['status'],
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256' )
        return token
    
    def parse_token(token):
        """
            Decodes the JWT token and returns the data if the token is valid.
            
            :param token: JWT token as a string
            :return: Decoded data as a dictionary if the token is valid, else None
        """
        try:
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_data
        except jwt.ExpiredSignatureError:
            print("Token has expired!")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token!")
            return None
        
        
    
# user_info = {
#     'name' : 'Kaushal',
#     'email' : 'kaushal@gmail.com',
#     'role' : 'MASTER',
# }

# print(JwtConfigService.generate_jwt_token(user_info))

# print('Parsed Token :: ',JwtConfigService.parse_token(JwtConfigService.generate_jwt_token(user_info)))
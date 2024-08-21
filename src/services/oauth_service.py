from pymongo import MongoClient

class OAuthService:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://genai:genaipass@localhost:27017/')
        self.db = self.client['user_db']  # Automatically create the database
        self.collection = self.db['users']  # Automatically create the collection

    def save_user(self, user_data):
        """
        Save user data into MongoDB.
        
        :param user_data: Dictionary containing user information.
        :return: A response indicating success or failure.
        """
        try:
            # Insert the user data into the collection
            result = self.collection.insert_one(user_data)
            return {"status": "success", "user_id": str(result.inserted_id)}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def retrieve_user(self, identifier):
        """
        Retrieve user data based on email, username, or name.
        
        :param identifier: The value to search for in 'email', 'username', or 'name' fields.
        :return: The user data document if found, else None.
        """
        query = {"$or": [
            {"email": identifier},
            {"username": identifier},
            {"name": identifier}
        ]}
        
        user_data = self.collection.find_one(query)

        if user_data:
            # Remove the ObjectId field before returning the result
            user_data.pop('_id', None)
            
        return user_data
    
    def update_user(self, identifier, update_data):
        """
        Update user data based on email, username, or name.
        
        :param identifier: The value to search for in 'email', 'username', or 'name' fields.
        :param update_data: Dictionary containing the fields to update.
        :return: A response indicating success or failure.
        """
        query = {"$or": [
            {"email": identifier},
            {"username": identifier},
            {"name": identifier}
        ]}

        try:
            result = self.collection.update_one(query, {"$set": update_data})
            if result.matched_count > 0:
                return {"status": "success", "modified_count": result.modified_count}
            else:
                return {"status": "failure", "message": "User not found"}
        except Exception as e:
            return {"status": "failure", "error": str(e)}


# Save a new user
# user = {
#     "username": "genai",
#     "email": "genai@example.com",
#     "name": "Gen AI",
#     "other_field": "example_value"
# }

# print('user :: ', user)

# oauth_service = OAuthService()

# Save the user and get a response
# response = oauth_service.save_user(user)
# print('response :: ', response)

# Retrieve the user by email, username, or name
# retrieved_user = oauth_service.retrieve_user("genai1@example.com")
# if(retrieved_user is None):
#     print('Not fount')
# else:
#     print('retrieved user :: ', retrieved_user)

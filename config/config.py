import os

class Config:
    MONGO_URL = os.getenv("MONGO_URL") or 'mongodb://admin:password@localhost:27017/?authSource=admin'
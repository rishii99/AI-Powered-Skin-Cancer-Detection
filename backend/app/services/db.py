from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
db = client.get_database()

users_collection = db.get_collection('users')
predictions_collection = db.get_collection('predictions')
feedback_collection = db.get_collection('feedback')

# Ensure indexes for performance and duplicate detection
users_collection.create_index('email', unique=True)
predictions_collection.create_index('user_id')
predictions_collection.create_index('created_at')
feedback_collection.create_index('prediction_id')

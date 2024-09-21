from pymongo import MongoClient
from src.config.settings import MONGO_URI, DB_NAME

def setup_mongo_client():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db['page_contents'], db['extracted_links'], db['detailed_pages']

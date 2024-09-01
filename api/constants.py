import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_USER = os.environ.get('MONGO_DB_USER')
MONGO_DB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')
MONGO_DB_CLUSTER_URL = os.environ.get('MONGO_DB_CLUSTER_URL')
MONGO_DB_APP_NAME = os.environ.get('MONGO_DB_APP_NAME')
MAX_PAGE_SIZE = os.environ.get('MAX_PAGE_SIZE', 200)
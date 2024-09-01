import motor.motor_asyncio
from api.constants import (
    MONGO_DB_USER,
    MONGO_DB_PASSWORD,
    MONGO_DB_CLUSTER_URL,
    MONGO_DB_APP_NAME
)

mongo_db_url = "mongodb+srv://"
mongo_db_url += MONGO_DB_USER + ":"
mongo_db_url += MONGO_DB_PASSWORD + "@"
mongo_db_url += MONGO_DB_CLUSTER_URL + "/?retryWrites=true&w=majority&appName="
mongo_db_url += MONGO_DB_APP_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_db_url)

db = client.ecommerce_db
users_collection = db["users_data"]
products_collection = db["products_data"]
shopping_carts_collection = db["shopping_carts_data"]

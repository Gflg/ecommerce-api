import sys

sys.path.append('..')

from fastapi import FastAPI
from api.routers import products, shopping_carts, users


app = FastAPI()
app.include_router(products.router)
app.include_router(users.router)
app.include_router(shopping_carts.router)

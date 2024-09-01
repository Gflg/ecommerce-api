from typing import List
from pydantic import BaseModel

from api.enums import ProductType


class User(BaseModel):
    '''User model with its attributes.'''
    username: str
    email: str
    password: str


class Product(BaseModel):
    '''Product model with its attributes.'''
    name: str
    theme: ProductType
    price: float
    quantity: int


class ProductInCart(BaseModel):
    '''ProductInCart model with its attributes.'''
    product_id: str
    quantity: int


class ShoppingCart(BaseModel):
    '''ShoppingCart model with its attributes.'''
    user_id: str
    products: List[ProductInCart]

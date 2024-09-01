from typing import List
from pydantic import BaseModel
from api.enums import ProductType
from api.db.models import ProductInCart


class CreateOutput(BaseModel):
    '''Schema used as response models in POST endpoints.'''
    id: str


class CreateUserOutput(BaseModel):
    '''Schema used as a response model in POST /api/users/ endpoint.'''
    id: str
    shopping_cart_id: str


class GetUserOutput(BaseModel):
    '''Schema used as a response model in GET users endpoints.'''
    id: str
    username: str
    email: str


class UpdateOutput(BaseModel):
    '''Schema used as response models in PUT/PATCH endpoints.'''
    message: str


class UpdateUserPasswordInput(BaseModel):
    '''Schema used as an input model in
    PATCH /api/users/{user_id} endpoint.
    '''
    password: str


class GetProductOutput(BaseModel):
    '''Schema used as a response model in GET products endpoints.'''
    id: str
    name: str
    theme: ProductType
    price: float
    quantity: int


class UpdateProductStockInput(BaseModel):
    '''Schema used as an input model in
    PATCH /api/products/{product_id} endpoint.
    '''
    quantity: int


class CreateEmptyShoppingCartInput(BaseModel):
    '''Schema used as an input model in
    POST /api/shopping_carts/ endpoint.
    '''
    user_id: str


class GetShoppingCartOutput(BaseModel):
    '''Schema used as a response model in GET shopping_carts endpoints.'''
    id: str
    user_id: str
    products: List[ProductInCart]

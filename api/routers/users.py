from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from api.constants import MAX_PAGE_SIZE
from api.db.actions import (
    create_obj,
    delete_obj,
    find_obj_by_id,
    update_obj
)
from api.db.models import User
from api.db.settings import (
    users_collection,
    shopping_carts_collection
)
from api.db.schemas import (
    CreateUserOutput,
    GetUserOutput,
    UpdateOutput,
    UpdateUserPasswordInput
)

router = APIRouter()


@router.post("/api/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: User) -> CreateUserOutput:
    '''
    Endpoint used to create a new user.
    It also creates a shopping cart linked to the new user.
    '''
    user = await create_obj(users_collection, dict(user_data))
    shopping_cart_dict = {
        "user_id": user.inserted_id,
        "products": []
    }
    shopping_cart = await create_obj(
        shopping_carts_collection,
        shopping_cart_dict
    )

    return {
        'id': str(user.inserted_id),
        'shopping_cart_id': str(shopping_cart.inserted_id)
    }


@router.get("/api/users/", status_code=status.HTTP_200_OK)
async def get_users(
        skip: int,
        limit: int) -> List[GetUserOutput]:
    '''
    Endpoint used to retrieve many users, according to the pagination,
    sorting and filtering settings. This endpoint can't return more than
    200 registers by default. This value can be changed in .env file.
    '''
    if limit > MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=422,
            detail="The number of registers in a page cannot exceed 200."
        )

    users = users_collection.find().skip(skip).limit(limit)

    response = []

    async for user in users:
        user_dict = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
        response.append(user_dict)

    return response


@router.get("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def find_user_by_id(user_id: str) -> GetUserOutput:
    '''Endpoint used to retrieve a single user by its identifier.'''
    try:
        id = ObjectId(user_id)
        user = await find_obj_by_id(users_collection, id)
        response = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    return response


@router.delete("/api/users/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: str):
    '''
    Endpoint used to delete a single user by its identifier.
    When deleting an user with shopping carts, this method ensures 
    that all linked shopping carts are deleted as well.
    '''
    try:
        id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=422, detail="User not valid")

    try:
        user = await find_obj_by_id(users_collection, id)
        await delete_obj(users_collection, user['_id'])
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    shopping_carts = shopping_carts_collection.find(
        {"user_id": ObjectId(user_id)}
    )
    async for shopping_cart in shopping_carts:
        await delete_obj(shopping_carts_collection, shopping_cart['_id'])


@router.put("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_data_by_id(
        user_id: str,
        user_data: User) -> UpdateOutput:
    '''Endpoint used to update all data of given user.'''
    try:
        id = ObjectId(user_id)
        user = await find_obj_by_id(users_collection, id)
        await update_obj(users_collection, user['_id'], dict(user_data))
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    return {'message': 'User updated successfully'}


@router.patch("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_password_by_user_id(
        user_id: str,
        user_data: UpdateUserPasswordInput) -> UpdateOutput:
    '''Endpoint used to change the password of a given user.'''
    try:
        id = ObjectId(user_id)
        user = await find_obj_by_id(users_collection, id)
        user['password'] = user_data.password
        await update_obj(users_collection, user['_id'], user)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    return {'message': 'User password updated successfully'}

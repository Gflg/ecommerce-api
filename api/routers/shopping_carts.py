from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from api.db.actions import (
    create_obj,
    delete_obj,
    find_obj_by_id,
    update_obj
)
from api.db.models import ProductInCart
from api.db.settings import (
    products_collection,
    shopping_carts_collection,
    users_collection
)
from api.db.schemas import (
    CreateOutput,
    GetShoppingCartOutput,
    CreateEmptyShoppingCartInput,
    UpdateOutput
)

router = APIRouter()


@router.post("/api/shopping_carts/", status_code=status.HTTP_201_CREATED)
async def create_shopping_cart(
        shopping_cart_data: CreateEmptyShoppingCartInput
        ) -> CreateOutput:
    '''Endpoint used to create an empty shopping cart linked to an user.'''
    shopping_cart_dict = dict(shopping_cart_data)
    shopping_cart_dict['products'] = []

    try:
        user_id = ObjectId(shopping_cart_dict['user_id'])
        shopping_cart_dict['user_id'] = user_id
    except Exception:
        raise HTTPException(status_code=422, detail="User not valid")

    user = await find_obj_by_id(users_collection, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    shopping_cart = await create_obj(
        shopping_carts_collection,
        shopping_cart_dict
    )

    return {'id': str(shopping_cart.inserted_id)}


@router.get("/api/shopping_carts/{shopping_cart_id}",
            status_code=status.HTTP_200_OK)
async def get_shopping_cart_by_id(
        shopping_cart_id: str) -> GetShoppingCartOutput:
    '''Endpoint used to retrieve a single shopping cart by its identifier.'''
    try:
        id = ObjectId(shopping_cart_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Shopping cart not valid")

    try:
        shopping_cart = await find_obj_by_id(shopping_carts_collection, id)
        shopping_cart_products = shopping_cart['products']
    except Exception:
        raise HTTPException(status_code=404, detail="Shopping cart not found")

    for product in shopping_cart_products:
        product['product_id'] = str(product['product_id'])

    response = {
        'id': str(shopping_cart['_id']),
        'user_id': str(shopping_cart['user_id']),
        'products': shopping_cart['products']
    }

    return response


@router.delete("/api/shopping_carts/{shopping_cart_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_shopping_cart_by_id(shopping_cart_id: str):
    '''Endpoint used to delete a shopping cart.'''
    try:
        id = ObjectId(shopping_cart_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Shopping cart not valid")

    try:
        shopping_cart = await find_obj_by_id(shopping_carts_collection, id)
        await delete_obj(shopping_carts_collection, shopping_cart['_id'])
    except Exception:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    

@router.patch("/api/shopping_carts/{shopping_cart_id}/clear",
              status_code=status.HTTP_200_OK)
async def clear_shopping_cart(
        shopping_cart_id: str) -> UpdateOutput:
    '''Endpoint used to remove all items from a shopping cart.'''
    try:
        id = ObjectId(shopping_cart_id)
        shopping_cart = await find_obj_by_id(shopping_carts_collection, id)
        shopping_cart['products'] = []
        await update_obj(
            shopping_carts_collection,
            shopping_cart['_id'],
            shopping_cart
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Shopping cart not found")

    return {'message': 'Shopping cart cleared successfully'}


@router.patch("/api/shopping_carts/{shopping_cart_id}/add_item",
              status_code=status.HTTP_200_OK)
async def add_items_to_shopping_cart(
        shopping_cart_id: str,
        products_data: List[ProductInCart]) -> UpdateOutput:
    '''
    Endpoint used to add items to a shopping cart.
    It validates a few things:
        1. If the shopping cart exists in the database
        2. If the product exists in the database
        3. If the product has enough stock to be added to the cart
    If all validations are successful, the cart will add all the items
    specified in the request's body.
    '''
    try:
        id = ObjectId(shopping_cart_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Shopping cart not valid")
    
    try:
        shopping_cart = await find_obj_by_id(shopping_carts_collection, id)
        current_products_in_cart = shopping_cart['products']
    except Exception:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    for product_data in products_data:
        product_data.product_id = ObjectId(product_data.product_id)
        try:
            id = product_data.product_id
            product = await find_obj_by_id(products_collection, id)
            product_quantity_in_stock = product['quantity'] 
        except Exception:
            raise HTTPException(status_code=404, detail="Product not found")
        
        is_product_already_in_cart = False
        quantity = product_data.quantity
        for product_in_cart in current_products_in_cart:
            if product_data.product_id == product_in_cart['product_id']:
                quantity += product_in_cart['quantity']
                is_product_already_in_cart = True
                break
        
        if quantity > product_quantity_in_stock:
            product_id = product_data.product_id
            msg = f"Product with ID {product_id} doesn't have enough stock"
            raise HTTPException(
                status_code=422,
                detail=msg
            )
        
        if not is_product_already_in_cart:
            current_products_in_cart.append({
                'product_id': product_data.product_id,
                'quantity': product_data.quantity
            })
        else:
            product_in_cart['quantity'] = quantity
    
    shopping_cart['products'] = current_products_in_cart
    await update_obj(
        shopping_carts_collection,
        shopping_cart['_id'],
        shopping_cart
    )

    return {'message': 'Items were added to shopping cart successfully'}


@router.patch("/api/shopping_carts/{shopping_cart_id}/remove_item",
              status_code=status.HTTP_200_OK)
async def remove_items_from_shopping_cart(
        shopping_cart_id: str,
        products_data: List[ProductInCart]) -> UpdateOutput:
    '''
    Endpoint used to remove items from a shopping cart.
    It validates a few things:
        1. If the shopping cart exists in the database
        2. If the product exists in the database
        3. If the product is in the given cart
    If all validations are successful, all specified items in the request's
    body will be removed from the given shopping cart.
    '''
    try:
        id = ObjectId(shopping_cart_id)
        shopping_cart = await find_obj_by_id(shopping_carts_collection, id)
        current_products_in_cart = shopping_cart['products']
    except Exception:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    products_to_remove_from_cart = []
    for product_data in products_data:
        try:
            id = ObjectId(product_data.product_id)
            product = await find_obj_by_id(products_collection, id)
            product_id = str(product['_id'])
        except Exception:
            raise HTTPException(status_code=404, detail="Product not found")
        
        is_product_already_in_cart = False
        quantity_in_cart = 0
        for product_in_cart in current_products_in_cart:
            if product_data.product_id == str(product_in_cart['product_id']):
                quantity_in_cart = product_in_cart['quantity']
                is_product_already_in_cart = True
                break
        
        if not is_product_already_in_cart:
            raise HTTPException(
                status_code=422,
                detail="Product isn't in shopping cart"
            )

        if quantity_in_cart < product_data.quantity:
            msg = f"Product with ID {product_id} has less units in cart"
            raise HTTPException(
                status_code=422,
                detail=msg)

        new_quantity = quantity_in_cart - product_data.quantity
        if new_quantity == 0:
            products_to_remove_from_cart.append(product_in_cart)
        else:
            product_in_cart['quantity'] = new_quantity
    
    for product in products_to_remove_from_cart:
        current_products_in_cart.remove(product)
    
    shopping_cart['products'] = current_products_in_cart
    await update_obj(
        shopping_carts_collection,
        shopping_cart['_id'],
        shopping_cart
    )

    return {'message': 'Items were removed from shopping cart successfully'}

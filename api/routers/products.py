from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from api.constants import MAX_PAGE_SIZE
from api.db.actions import (
    create_obj,
    delete_obj,
    find_obj_by_id,
    update_obj
)
from api.db.models import Product
from api.db.settings import products_collection, shopping_carts_collection
from api.db.schemas import (
    CreateOutput,
    GetProductOutput,
    UpdateOutput,
    UpdateProductStockInput
)
from api.routers.query_params import QueryParams

router = APIRouter()


@router.post("/api/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: Product) -> CreateOutput:
    '''Endpoint used to create a new product.'''
    product = await create_obj(products_collection, dict(product_data))

    return {'id': str(product.inserted_id)}


@router.get("/api/products/", status_code=status.HTTP_200_OK)
async def get_products(
        skip: int,
        limit: int,
        params: QueryParams = Depends()) -> List[GetProductOutput]:
    '''
    Endpoint used to retrieve many products, according to the pagination,
    sorting and filtering settings. This endpoint can't return more than
    200 registers by default. This value can be changed in .env file.
    '''
    if limit > MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=422,
            detail="The number of registers in a page cannot exceed 200."
        )

    query_filter = {}
    
    if params.apply_product_theme_filter:
        product_theme = params.product_theme
        query_filter['theme'] = product_theme.value
    
    products = products_collection.find(query_filter).skip(skip).limit(limit)

    if params.apply_product_attribute_sort:
        column_name = params.product_attribute_to_sort.value
        descending_value = -1 if params.descending else 1
        sort_filter = {column_name: descending_value}
        products = products.sort(sort_filter)
    
    response = []

    async for product in products:
        product_dict = {
            'id': str(product['_id']),
            'name': product['name'],
            'theme': product['theme'],
            'price': product['price'],
            'quantity': product['quantity']
        }
        response.append(product_dict)

    return response


@router.get("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def find_product_by_id(product_id: str) -> GetProductOutput:
    '''Endpoint used to retrieve a single product by its identifier.'''
    try:
        id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Product not valid")
    
    try:
        product = await find_obj_by_id(products_collection, id)
        response = {
            'id': str(product['_id']),
            'name': product['name'],
            'theme': product['theme'],
            'price': product['price'],
            'quantity': product['quantity']
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

    return response


@router.delete("/api/products/{product_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(product_id: str):
    '''
    Endpoint used to delete a single product by its identifier.
    When deleting a product already being used in shopping carts,
    this method ensures that all references of the excluded product
    are deleted from existing shopping carts.
    '''
    try:
        id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Product not valid")

    try:
        product = await find_obj_by_id(products_collection, id)
        await delete_obj(products_collection, product['_id'])
    except Exception: 
        raise HTTPException(status_code=404, detail="Product not found")

    shopping_carts = shopping_carts_collection.find(
        {"products": {"$elemMatch": {"product_id": ObjectId(product_id)}}}
    )
    async for shopping_cart in shopping_carts:
        for product in shopping_cart['products']:
            if product['product_id'] == ObjectId(product_id):
                shopping_cart['products'].remove(product)
                await update_obj(shopping_carts_collection, shopping_cart['_id'], shopping_cart)
                break


@router.put("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_data_by_id(
        product_id: str,
        product_data: Product) -> UpdateOutput:
    '''Endpoint used to update all data of given product.'''
    try:
        id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Product not valid")

    try:
        product = await find_obj_by_id(products_collection, id)
        await update_obj(
            products_collection,
            product['_id'],
            dict(product_data)
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

    return {'message': 'Product updated successfully'}


@router.patch("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_stock_by_product_id(
        product_id: str,
        product_data: UpdateProductStockInput) -> UpdateOutput:
    '''Endpoint used to change the stock of a given product.'''
    try:
        id = ObjectId(product_id)
        product = await find_obj_by_id(products_collection, id)
        product['quantity'] = product_data.quantity
        await update_obj(
            products_collection,
            product['_id'],
            product
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

    return {'message': 'Product stock updated successfully'}

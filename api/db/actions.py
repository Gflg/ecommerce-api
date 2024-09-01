from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


async def delete_obj(collection: AsyncIOMotorCollection, id: str):
    '''Delete object from any collection.'''
    await collection.delete_one({"_id": id})


async def find_obj_by_id(collection: AsyncIOMotorCollection, id: str):
    '''Find object by id in any collection.'''
    return await collection.find_one({"_id": id})


async def create_obj(collection: AsyncIOMotorCollection, data: dict):
    '''Create object in any collection.'''
    return await collection.insert_one(data)


async def update_obj(
        collection: AsyncIOMotorCollection,
        obj_id: str,
        new_obj: dict):
    '''Update object from any collection.'''
    return await collection.update_one({"_id": obj_id}, {"$set": new_obj})

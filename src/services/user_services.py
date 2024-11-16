from db import getDb
from bson import ObjectId
from model.User import User

database = getDb()
collection_user = database['User']

def add_user(user: User):
    if collection_user.find_one({'username': user.username}):
        return False
    else:
        collection_user.insert_one(user.to_schema())
        return True

def get_users():
    users = collection_user.find({})
    return [{**user, "_id": str(user["_id"])} for user  in users]

def check_user(username, password):
    data = collection_user.find_one({'username': username, 'password': password})
    if data:
        return {"_id": str(data["_id"]), "username": data["username"], "name": data["name"],"role": data["role"]}
    else :
        return False
    
def get_user(_id):
    data = collection_user.find_one({'_id': ObjectId(_id)})
    return {**data, "_id": str(data["_id"])}

def update_user(_id, name , password):
    collection_user.update_one(
        {'_id': ObjectId(_id)},
        {'$set': {'password': password, 'name': name}}
    )

def update_image(_id, image1, image2,idImage1,idImage2):
    collection_user.update_one(
        {'_id': ObjectId(_id)},
        {'$set': {'image1': image1,'image2': image2,'idImage1': idImage1,'idImage2': idImage2}}
    )

def delete_user(_id):
    collection_user.delete_one({'_id': ObjectId(_id)})
        


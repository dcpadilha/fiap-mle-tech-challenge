from pymongo import MongoClient


def show_collections():
    client = MongoClient('mongodb://172.23.0.1:27017')
    db = client['embrapa']
    print(f'Collections: {db["users"].find_one()}')
    return db['users'].find()

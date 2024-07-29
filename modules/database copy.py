import os

from pymongo import MongoClient


class Database:
    def __init__(self):
        return

    def connect(self):
        self.client = MongoClient(os.getenv('MONGODB_HOST'))
        self.db = self.client[os.getenv('MONGODB_DATABASE')]

    def get_scrape_links(self):
        return self.db['scrape_target'].find_one()

    def get_user_info(self, query):
        return self.db['users'].find_one(query)

    def add_user(self, user_info):
        new_user = {'user': user_info.user, 'password': user_info.password, 'email': user_info.email}

        self.db['users'].insert_one(new_user)

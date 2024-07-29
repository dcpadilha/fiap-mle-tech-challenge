import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from modules.models import ScrapeTarget, User


class Database:
    def connect(self):
        # Create an engine
        self.engine = create_engine(f"{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}")

        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user_info):
        new_user = User(user=user_info.user, password=user_info.password, email=user_info.email)

        self.session.add(new_user)
        self.session.commit()

    def get_scrape_links(self):
        results = self.session.scalars(select(ScrapeTarget))

        print(f'ScrapeResult: {results}')

        targets = {}

        for result in results:
            targets[result.target] = result.url

        return targets

    def get_user_info(self, query):
        search_user = query['user']
        print(f'SearchUser: {search_user}')
        result_user = self.session.scalar(select(User).where(User.user == search_user))

        print(f'Result: {result_user}')

        return {'user': result_user.user, 'password': result_user.password, 'email': result_user.email}


# from pymongo import MongoClient
# import os

# class Database():
#     def __init__(self):
#         return

#     def connect(self):
#         self.client = MongoClient(os.getenv('MONGODB_HOST'))
#         self.db = self.client[os.getenv('MONGODB_DATABASE')]

#     def get_scrape_links(self):
#         return self.db['scrape_target'].find_one()

#     def get_user_info(self, query):
#         return self.db['users'].find_one(query)

#     def add_user(self, user_info):
#         new_user = {
#             'user':  user_info.user,
#             'password': user_info.password,
#             'email': user_info.email
#         }

#         self.db['users'].insert_one(new_user)

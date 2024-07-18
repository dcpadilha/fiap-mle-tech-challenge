import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

from modules.routes import router

# Loads variables from .env file, but does not overwrite existing ones
# Not overwriting will support dockerization in the future (hopefully)
# Environment variables will be provided by static .env file or by arguments
load_dotenv(override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates MongoDB connection during application startup
    app.mongodb_client = MongoClient(os.getenv('MONGODB_HOST'))
    app.database = app.mongodb_client[os.getenv('MONGODB_COLLECTION')]

    yield
    # Closes MongoDB connection on application shutdown
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router, tags=['endpoints'])

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from modules.database import Database

# User Modules
from modules.routes import router

# Loads variables from .env file
load_dotenv(override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connects to the database and creates a session that will be available for the other modules
    app.database = Database()
    app.database.connect()

    yield
    # Closes the database session
    app.database.session.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router, tags=['endpoints'])

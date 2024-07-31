from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth_controller, vitibrasil_controller, dags_airflow_controller
import logging
from util import get_logger, clone_log_config

origins = ["*"]
methods = ["*"]
headers = ["*"]

app = FastAPI()

app.include_router(vitibrasil_controller.router)
app.include_router(auth_controller.router)
app.include_router(dags_airflow_controller.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True,
)

@app.on_event("startup")
async def load_stores():
    logger = get_logger(__file__)

    server_logger = logging.getLogger("uvicorn")
    clone_log_config(logger, server_logger)
    server_logger = logging.getLogger("uvicorn.access")
    clone_log_config(logger, server_logger)
    server_logger = logging.getLogger("uvicorn.error")
    clone_log_config(logger, server_logger)
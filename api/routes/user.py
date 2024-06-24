from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/v1")

@router.get("/users/{username}")
async def read_user(username: str):
    return JSONResponse(jsonable_encoder({ 'message': 'OK'}), 200)
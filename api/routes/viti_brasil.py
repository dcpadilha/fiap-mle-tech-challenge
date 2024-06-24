from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/v1")

@router.get("/vitibrasil/{type}")
async def get_info_vitibrasil(type: str):

    return JSONResponse(jsonable_encoder({ 'message': 'OK'}), 200)


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import timedelta
from config.jwt import create_access_token, Token

router = APIRouter(prefix="/api/v1")

class UserLogin(BaseModel):
    username: str

@router.post("/token", response_model=Token)
def login(user: UserLogin):
    if not user.username:
        raise HTTPException(status_code=422, detail="Username is required")
    
    # No mundo real, você deve verificar a senha do usuário
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
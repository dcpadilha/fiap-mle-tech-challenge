from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from interfaces import ivitibrasil_repository
from repositories import vitibrasil_repository
from config.database import SessionLocal
from typing import List, Optional
from config.jwt import get_current_user, TokenData


router = APIRouter(prefix="/api/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/vitibrasil/", response_model=List[ivitibrasil_repository.VitiBrasilInDB])
def read_vitibrasil(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vitibrasil = vitibrasil_repository.get_all_vitibrasil(db)
    return vitibrasil

@router.get("/vitibrasil/{id}", response_model=ivitibrasil_repository.VitiBrasilInDB)
def read_vitibrasil(id: int, db: Session = Depends(get_db)):
    vitibrasil = vitibrasil_repository.get_vitibrasil_by_id(db, id)
    if vitibrasil is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return vitibrasil

@router.get("/vitibrasil/categoria/", response_model=List[ivitibrasil_repository.VitiBrasilInDB])
def read_vitibrasil(
    skip: int = 0,
    limit: int = 10,
    categoria: Optional[str] = None,
    ano_min: Optional[str] = None,
    ano_max: Optional[str] = None,
    db: Session = Depends(get_db),
    authorization: TokenData = Depends(get_current_user) 
):

    if categoria:
        vitibrasil = vitibrasil_repository.get_vitibrasil_by_categoria_and_year_range(
            db, categoria, ano_min=ano_min, ano_max=ano_max, skip=skip, limit=limit
        )
    else:
        vitibrasil = vitibrasil_repository.get_all_vitibrasil(db, skip=skip, limit=limit)
    
    if not vitibrasil:
        raise HTTPException(status_code=404, detail="No items found")
    
    return vitibrasil

@router.get("/vitibrasil/origem/", response_model=List[ivitibrasil_repository.VitiBrasilInDB])
def read_vitibrasil(
    skip: int = 0,
    limit: int = 10,
    origem: Optional[str] = None,
    ano_min: Optional[str] = None,
    ano_max: Optional[str] = None,
    db: Session = Depends(get_db),
    authorization: TokenData = Depends(get_current_user)
):
    if origem:
        vitibrasil = vitibrasil_repository.get_vitibrasil_by_origem_and_year_range(
            db, origem, ano_min=ano_min, ano_max=ano_max, skip=skip, limit=limit
        )
    else:
        vitibrasil = vitibrasil_repository.get_all_vitibrasil(db, skip=skip, limit=limit)
    
    if not vitibrasil:
        raise HTTPException(status_code=404, detail="No items found")
    
    return vitibrasil
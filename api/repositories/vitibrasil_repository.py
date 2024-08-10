from sqlalchemy.orm import Session
from models.vitbrasil import VitiBrasil
from typing import Optional

def get_all_vitibrasil(db: Session):
    return db.query(VitiBrasil).all()

def get_vitibrasil_by_id(db: Session, vitibrasil_id: int):
    return db.query(VitiBrasil).filter(VitiBrasil.id == vitibrasil_id).first()

def get_vitibrasil_by_categoria_and_year_range(
    db: Session,
    categoria: str,
    ano_min: Optional[str] = None,
    ano_max: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(VitiBrasil).filter(VitiBrasil.categoria == categoria)
    
    if ano_min:
        query = query.filter(VitiBrasil.ano >= ano_min)
    if ano_max:
        query = query.filter(VitiBrasil.ano <= ano_max)
    
    return query.offset(skip).limit(limit).all()

# Função para buscar por origem e intervalo de anos com paginação
def get_vitibrasil_by_origem_and_year_range(
    db: Session,
    origem: str,
    ano_min: Optional[str] = None,
    ano_max: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(VitiBrasil).filter(VitiBrasil.origem == origem)
    
    if ano_min:
        query = query.filter(VitiBrasil.ano >= ano_min)
    if ano_max:
        query = query.filter(VitiBrasil.ano <= ano_max)
    
    return query.offset(skip).limit(limit).all()


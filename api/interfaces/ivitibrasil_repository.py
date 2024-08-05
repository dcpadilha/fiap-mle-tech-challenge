from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VitiBrasilBase(BaseModel):
    ano: Optional[str]
    origem: Optional[str]
    sub_origem: Optional[str]
    categoria: Optional[str]
    sub_categoria: Optional[str]
    valor: Optional[float]
    qtde_kg: Optional[int]

class VitiBrasilCreate(VitiBrasilBase):
    pass

class VitiBrasilUpdate(VitiBrasilBase):
    last_updated: datetime

class VitiBrasilInDB(VitiBrasilBase):
    id: int
    inserted_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True

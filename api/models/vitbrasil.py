from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VitiBrasil(Base):
    __tablename__ = 'vitibrasil'

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(String(4))
    origem = Column(String(100))
    sub_origem = Column(String(100))
    categoria = Column(String(100))
    sub_categoria = Column(String(100))
    valor = Column(DECIMAL(18, 2))
    qtde_kg = Column(Integer)
    inserted_at = Column(DateTime)
    last_updated = Column(DateTime, nullable=True)
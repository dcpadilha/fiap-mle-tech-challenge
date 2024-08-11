from sqlalchemy.orm import Session
from sqlalchemy import select
from models.vitbrasil import Usuario
from typing import Optional

# Função para buscar o usuário sendo autenticado
def get_usuario(
    db: Session,
    usuario: str
):
#   query = db.query(Usuario).filter(Usuario.usuario == usuario)
  query = db.scalar(select(Usuario).where(Usuario.usuario == usuario))

  if not query is None:
    usuario_encontrado = { 
            "usuario" : query.usuario,
            "senha" : query.senha,
            "role" : query.role
        }
    return usuario_encontrado
  else:
    return None
  
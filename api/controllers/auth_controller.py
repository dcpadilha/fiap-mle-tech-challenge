from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
from config.jwt import create_access_token, get_password_hash, verify_password,Token, UserData
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from repositories.auth_repository import get_usuario
from config.database import SessionLocal
from sqlalchemy.orm import Session
from models.vitbrasil import Usuario

router = APIRouter(prefix="/api/v1")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class UserLogin(BaseModel):
    usuario: str
    senha: str
    role: str

# Função usada para criar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint utilizado na autenticação do usuário e geração do token de acesso
@router.post("/token", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    # A informação do nome do usuário é obrigatória para a consulta ao banco de dados
    if not form_data.username:
        raise HTTPException(status_code=422, detail="Username is required")
    
    # Consultando o banco de dados em busca do usuário informado
    user = get_usuario(db,form_data.username)

    # Validando a existência do usuário
    if not user:
        raise HTTPException(
            status_code=422, 
            detail="Erro ao acessar usuário ao banco de dados"
        )    

    # Validando a senha do usuário
    if not verify_password(form_data.password, user['senha']):
        raise HTTPException(
            status_code=401,
            detail='Incorrect email or password',
        )
    
    # Definindo o tempo de expiração do token de acesso
    access_token_expires = timedelta(minutes=30)

    # Criação do token de acesso incluindo o perfil (role) do usuário 
    # que será utilizado na validação das autorizações
    access_token = create_access_token(
        data={"sub": user["usuario"], "role": user["role"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/user", response_model=UserData)
def add_user(user_info: UserLogin,db: Session = Depends(get_db)):
    user_info.senha = get_password_hash(user_info.senha)

    try:
        new_user = Usuario(usuario=user_info.usuario, senha=user_info.senha, role=user_info.role)
        db.add(new_user)
        db.commit()
        return {'user': user_info.usuario, 'role' : user_info.role}
    except Exception as e:
        raise HTTPException(status_code=422, detail="Erro ao adicionar usuário ao banco de dados")
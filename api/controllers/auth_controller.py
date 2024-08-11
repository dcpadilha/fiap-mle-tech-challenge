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
    """
    Autentica o usuário e retorna um token de acesso.

    **Endpoint:** `/token`

    **Método:** `POST`

    **Parâmetros:**

    - `db` (Session, opcional): Dependência da sessão do banco de dados. Injetada automaticamente.
    - `form_data` (OAuth2PasswordRequestForm): Dados do formulário de autenticação, incluindo nome de usuário e senha. Injetado automaticamente.

    **Corpo da Solicitação:**

    - `username` (str): Nome de usuário para autenticação.
    - `password` (str): Senha do usuário.

    **Respostas:**

    - `200 OK`: Retorna um token de acesso em formato JSON.
    - `422 Unprocessable Entity`: Se o nome de usuário não for fornecido ou se houver um erro ao acessar o usuário no banco de dados.
    - `401 Unauthorized`: Se o nome de usuário ou a senha estiverem incorretos.

    **Descrição:**
    Este endpoint permite que um usuário se autentique fornecendo seu nome de usuário e senha. Se as credenciais estiverem corretas, o sistema gera e retorna um token de acesso. Este token pode ser usado para autenticação em outras rotas que exigem um token de acesso válido.

    **Exemplo de Solicitação:**
    ```json
    POST /token
    {
        "username": "exemplo_usuario",
        "password": "senha_secreta"
    }
    ```

    **Exemplo de Resposta:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleGFtcGxldXN1YXJpbyIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjg2NTUzMzA3LCJleHBpcmF0aW9uIjoxNjg2NTUzNjA3fQ.5nP6qGJdqvG8aOxDw8_LD04T0G4X9IbsZ3eA7xMC7iw",
        "token_type": "bearer"
    }
    ```
    """


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


# Endpoint para criação de usuários
# Em um ambiente produtivo, este endpoint deveria estar protegido e o usuário ADMIN deveria ser criado de outra forma
@router.post("/user", response_model=UserData)
def add_user(user_info: UserLogin,db: Session = Depends(get_db)):
    """
    Adiciona um novo usuário ao banco de dados.

    **Endpoint:** `/user`

    **Método:** `POST`

    **Parâmetros:**

    - `user_info` (UserLogin): Dados do usuário a serem adicionados, incluindo nome de usuário, senha e função.

    **Corpo da Solicitação:**

    - `usuario` (str): Nome de usuário do novo usuário.
    - `senha` (str): Senha do novo usuário. A senha será criptografada antes de ser armazenada.
    - `role` (str): Função ou papel do novo usuário.

    **Respostas:**

    - `200 OK`: Retorna uma mensagem de sucesso indicando que o usuário foi adicionado com sucesso.
    - `422 Unprocessable Entity`: Se houver um erro ao adicionar o usuário no banco de dados.

    **Descrição:**
    Este endpoint permite a adição de um novo usuário ao banco de dados. O nome de usuário, senha e função devem ser fornecidos no corpo da solicitação. A senha é criptografada antes de ser armazenada para garantir a segurança. Se a adição do usuário for bem-sucedida, uma mensagem de sucesso será retornada. Caso contrário, será levantada uma exceção com uma mensagem de erro.

    **Exemplo de Solicitação:**
    ```json
    POST /user
    {
        "usuario": "admin",
        "senha": "admin",
        "role": "ADMIN"
    }
    ```

    **Exemplo de Resposta:**
    ```json
    {
        "message": "Usuário adicionado."
    }
    ```
    """

    user_info.senha = get_password_hash(user_info.senha)

    try:
        new_user = Usuario(usuario=user_info.usuario, senha=user_info.senha, role=user_info.role)
        db.add(new_user)
        db.commit()
        return {'user': user_info.usuario, 'role' : user_info.role}
    except Exception as e:
        raise HTTPException(status_code=422, detail="Erro ao adicionar usuário ao banco de dados")
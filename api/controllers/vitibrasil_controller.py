from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from interfaces import ivitibrasil_repository
from repositories import vitibrasil_repository
from config.database import SessionLocal
from typing import List, Optional
from config.jwt import get_current_user, TokenData
from models.vitbrasil import OrigemEnum


router = APIRouter(prefix="/api/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Este endpoint retorna todo o conteúdo do banco de dados que foi extraído através das DAGs
@router.get("/vitibrasil/", response_model=List[ivitibrasil_repository.VitiBrasilInDB])
def read_vitibrasil(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    authorization: TokenData = Depends(get_current_user)
):
    """
    Este endpoint retorna todo o conteúdo do banco de dados que foi extraído através das DAGs

    **Notas:**
    - Certifique-se de que a autenticação esteja configurada corretamente, pois o endpoint exige um token de autorização.
    """
    
    vitibrasil = vitibrasil_repository.get_all_vitibrasil(db)
    return vitibrasil

# Endpoint que retorna um único resultado baseado na chave primária (ID) do banco de dados
@router.get("/vitibrasil/{id}", response_model=ivitibrasil_repository.VitiBrasilInDB)
def read_vitibrasil(
    id: int, 
    db: Session = Depends(get_db), 
    authorization: TokenData = Depends(get_current_user
)):
    """
    Recupera um registro do VitiBrasil pelo ID.

    **Endpoint:** `/vitibrasil/{id}`

    **Método:** `GET`

    **Parâmetros:**

    - `id` (int): O ID do registro do VitiBrasil que deve ser recuperado.
    - `authorization` (TokenData, opcional): O token de autenticação do usuário. Injetado automaticamente.

    **Respostas:**

    - `200 OK`: Retorna o registro do VitiBrasil com o ID especificado. O registro adere ao modelo `VitiBrasilInDB`.
    - `404 Not Found`: Se o registro com o ID especificado não for encontrado no banco de dados.

    **Descrição:**
    Este endpoint permite a recuperação de um registro específico do VitiBrasil com base no ID fornecido. O ID do registro deve ser passado como um parâmetro na URL. Se um registro com o ID fornecido for encontrado, ele será retornado no formato definido pelo modelo `VitiBrasilInDB`. Caso contrário, será levantada uma exceção com uma mensagem de erro indicando que o item não foi encontrado.

    **Exemplo de Solicitação:**
    ```
    GET /vitibrasil/2
    ```

    **Exemplo de Resposta:**
    ```json
    {
        "ano": "1974",
        "origem": "Comercializacao",
        "sub_origem": "",
        "categoria": "VINHO DE MESA",
        "sub_categoria": "Rosado",
        "valor": null,
        "qtde_kg": 8891367,
        "id": 2,
        "inserted_at": "2024-08-11T17:59:27",
        "last_updated": "2024-08-11T20:59:27"
    }
    ```
    """
    
    vitibrasil = vitibrasil_repository.get_vitibrasil_by_id(db, id)
    if vitibrasil is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return vitibrasil

# Endpoint que retorna uma categoria específica
# É possível especificar o período, em anos, da consulta
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
    """
    Recupera uma lista de registros do VitiBrasil com base na categoria e no intervalo de anos.

    **Endpoint:** `/vitibrasil/categoria/`

    **Método:** `GET`

    **Parâmetros:**

    - `skip` (int, opcional): Default é 0.
    - `limit` (int, opcional): Número máximo de registros a serem retornados. Default é 10.
    - `categoria` (Optional[str], opcional): Categoria para filtrar os registros. Se fornecida, somente os registros com essa categoria serão retornados.
    - `ano_min` (Optional[str], opcional): Ano mínimo para filtrar os registros. Se fornecido, somente os registros a partir deste ano serão incluídos.
    - `ano_max` (Optional[str], opcional): Ano máximo para filtrar os registros. Se fornecido, somente os registros até este ano serão incluídos.
    - `authorization` (TokenData, opcional): O token de autenticação do usuário. Injetado automaticamente.

    **Respostas:**

    - `200 OK`: Retorna uma lista de registros do VitiBrasil que correspondem aos critérios de filtro. Cada registro adere ao modelo `VitiBrasilInDB`.
    - `404 Not Found`: Se nenhum registro corresponder aos critérios de filtro ou se não houver registros no banco de dados.

    **Descrição:**
    Este endpoint permite recuperar registros do VitiBrasil com base em uma categoria opcional e um intervalo de anos. Se uma categoria for fornecida, os registros serão filtrados por essa categoria. O intervalo de anos pode ser definido pelos parâmetros `ano_min` e `ano_max`. Se não forem fornecidos filtros, todos os registros serão retornados com base na paginação suportada pelos parâmetros `skip` e `limit`.

    **Exemplo de Solicitação:**
    ```
    GET vitibrasil/categoria/?skip=0&limit=2&categoria=Togo&ano_min=2020&ano_max=2023
    ```

    **Exemplo de Resposta:**
    ```json
    [
        {
            "ano": "2021",
            "origem": "Exportacao",
            "sub_origem": "Suco de Uva",
            "categoria": "Togo",
            "sub_categoria": "",
            "valor": 0,
            "qtde_kg": 0,
            "id": 14758,
            "inserted_at": "2023-01-01T00:00:00",
            "last_updated": "2024-08-11T21:04:16"
        },
        {
            "ano": "2022",
            "origem": "Exportacao",
            "sub_origem": "Suco de Uva",
            "categoria": "Togo",
            "sub_categoria": "",
            "valor": 0,
            "qtde_kg": 0,
            "id": 14774,
            "inserted_at": "2023-01-01T00:00:00",
            "last_updated": "2024-08-11T21:04:16"
        }
    ]
    ```
    """

    if categoria:
        vitibrasil = vitibrasil_repository.get_vitibrasil_by_categoria_and_year_range(
            db, categoria, ano_min=ano_min, ano_max=ano_max, skip=skip, limit=limit
        )
    else:
        vitibrasil = vitibrasil_repository.get_all_vitibrasil(db, skip=skip, limit=limit)
    
    if not vitibrasil:
        raise HTTPException(status_code=404, detail="No items found")
    
    return vitibrasil

# Endpoint que retorna resultados baseados na Origem
# É possível especificar o período, em anos, da consulta
@router.get("/vitibrasil/origem/", response_model=List[ivitibrasil_repository.VitiBrasilInDB])
def read_vitibrasil(
    skip: int = 0,
    limit: int = 10,
    origem: Optional[OrigemEnum] = None,
    ano_min: Optional[str] = None,
    ano_max: Optional[str] = None,
    db: Session = Depends(get_db),
    authorization: TokenData = Depends(get_current_user)
):
    """
    Essa rota permite filtrar somente a tabela origem do Vitibrasil.

    **Endpoint:** `/vitibrasil/origem/`

    **Método:** `GET`

    **Parâmetros:**
    
    - `skip` (int, optional): Default é 0.
    - `limit` (int, optional): O número máximo de registros que retornarão. Default é 10.
    - `origem` (Optional[OrigemEnum], optional): Filtro de registros baseado no campo 'origem'. Se fornecido, somente registros com esse filtro serão retornados
    - `ano_min` (Optional[str], optional): O ano mínimo para filtrar os registros. Se fornecido, somente registros a partir desse ano serão retornados.
    - `ano_max` (Optional[str], optional): O ano máximo para filtrar os registros. Se fornecido, somente registros abaixo desse ano serão retornados.
    - `authorization` (TokenData, optional): Token de autenticação do usuário. É inserido automaticamente se é feito o login no swagger.

    **Respostas:**

    - `200 OK`: Retorna os registros solicitados. 
    - `404 Not Found`: Se o registro não é encontrado na base de dados ou se o filtro passado não é reconhecido.

    **Descrição:**
    Este endpoint recupera registros do VitiBrasil do banco de dados. Os registros podem ser filtrados por 'origem' e intervalo de anos (`ano_min` a `ano_max`). Se nenhum filtro for aplicado, todos os registros serão recuperados com paginação suportada pelos parâmetros `skip` e `limit`.

    **Examplo de Request:**
    ```
    GET /vitibrasil/origem/?limit=10&origem=Exportacao&ano_min=2020&ano_max=2023
    ```

    **Example Response:**
    ```json
    [
        {
            "ano": "2020",
            "origem": "Exportacao",
            "sub_origem": "Espumantes",
            "categoria": "África do Sul",
            "sub_categoria": "",
            "valor": 0,
            "qtde_kg": 0,
            "id": 8013,
            "inserted_at": "2023-01-01T00:00:00",
            "last_updated": "2024-08-11T21:01:42"
        },
        {
            "ano": "2020",
            "origem": "Exportacao",
            "sub_origem": "Espumantes",
            "categoria": "Alemanha",
            "sub_categoria": "",
            "valor": 14767,
            "qtde_kg": 2388,
            "id": 8014,
            "inserted_at": "2023-01-01T00:00:00",
            "last_updated": "2024-08-11T21:01:42"
        }
    ]
    ```
    """

    if origem:
        vitibrasil = vitibrasil_repository.get_vitibrasil_by_origem_and_year_range(
            db, origem, ano_min=ano_min, ano_max=ano_max, skip=skip, limit=limit
        )
    else:
        vitibrasil = vitibrasil_repository.get_all_vitibrasil(db, skip=skip, limit=limit)
    
    if not vitibrasil:
        raise HTTPException(status_code=404, detail="No items found")
    
    return vitibrasil
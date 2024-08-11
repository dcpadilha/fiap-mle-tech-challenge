from fastapi import APIRouter, Depends, HTTPException
import requests
from config.jwt import get_current_user, TokenData

# Endpoint do AirFlow que retorna as DAGs disponíveis
AIRFLOW_API_URL = "http://airflow-webserver:8080/api/v1/dags"

# Criação do roteador utilizado para prefixar os endpoints da API
router = APIRouter(prefix="/api/v1")

# Valores utilizados na autenticação da API do AirFlow
# Em um ambiente produtivo essa informação deve ser protegida
AUTH = ('airflow', 'airflow')

# Endpoint que consulta do AirFlow para retornar as DAGs disponíveis
@router.get("/airflow/dags/")
def get_dags(
    authorization: TokenData = Depends(get_current_user)
):
    
    # Este endpoint, além da autenticação, valida se o usuário possui o perfil necessário
    if authorization.role != 'ADMIN':
        raise HTTPException(
            status_code=401, 
            detail=f"Usuário {authorization.username} não está autorizado (somente perfil ADMIN). Perfil atual: {authorization.role}"
        )
    try:
        # Chamada ao endpoint do Airflow que lista as DAGs existentes
        response = requests.get(AIRFLOW_API_URL, auth=AUTH)
        response.raise_for_status()  # Levanta um erro se a resposta não for 2xx
        dags = response.json()
        
        # Extraindo os nomes das DAGs
        dag_names = [dag['dag_id'] for dag in dags.get('dags', [])]
        return {"dag_names": dag_names}
    
    # Avaliação das possíveis exceções
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
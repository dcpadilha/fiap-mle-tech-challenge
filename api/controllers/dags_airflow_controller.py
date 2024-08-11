from fastapi import APIRouter, Depends, HTTPException
import requests
from config.jwt import get_current_user, TokenData


AIRFLOW_API_URL = "http://airflow-webserver:8080/api/v1/dags"

router = APIRouter(prefix="/api/v1")

AUTH = ('airflow', 'airflow')


@router.get("/airflow/dags/")
def get_dags(
    authorization: TokenData = Depends(get_current_user)
):
    if authorization.role != 'ADMIN':
        raise HTTPException(status_code=401, detail=f"Usuário {authorization.username} não está autorizado (somente perfil ADMIN). Perfil atual: {authorization.role}")
    try:
        response = requests.get(AIRFLOW_API_URL, auth=AUTH)
        response.raise_for_status()  # Levanta um erro se a resposta não for 2xx
        dags = response.json()
        
        # Extraindo os nomes das DAGs
        dag_names = [dag['dag_id'] for dag in dags.get('dags', [])]
        return {"dag_names": dag_names}
    
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
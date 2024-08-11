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
    """
    Recupera a lista de DAGs (Directed Acyclic Graphs) do Airflow.

    **Endpoint:** `/airflow/dags/`

    **Método:** `GET`

    **Parâmetros:**

    - `authorization` (TokenData, opcional): O token de autenticação do usuário. Injetado automaticamente.

    **Respostas:**

    - `200 OK`: Retorna uma lista de nomes das DAGs do Airflow.
    - `401 Unauthorized`: Se o usuário não tiver o perfil `ADMIN` necessário para acessar as DAGs.
    - `500 Internal Server Error`: Se ocorrer um erro ao tentar recuperar os dados do Airflow.

    **Descrição:**
    Este endpoint recupera a lista de DAGs do Airflow. Para acessar esta rota, o usuário precisa ter o perfil `ADMIN`. Se o usuário não tiver as permissões necessárias, será levantada uma exceção com uma mensagem de autorização. Caso a autorização seja válida, a rota faz uma requisição para a API do Airflow e retorna os nomes das DAGs disponíveis. Em caso de falha na comunicação com a API do Airflow ou em outros erros, será levantada uma exceção com uma mensagem apropriada.

    **Exemplo de Solicitação:**
    ```
    GET /airflow/dags/
    ```

    **Exemplo de Resposta:**
    ```json
    {
        "dag_names": [
            "dag_vitbrasil_extract_commercialization",
            "dag_vitbrasil_extract_exportation_espumantes",
            "dag_vitbrasil_extract_exportation_suco_uva",
            "dag_vitbrasil_extract_exportation_uvas_frescas",
            "dag_vitbrasil_extract_exportation_vinhos_mesa",
            "dag_vitbrasil_extract_importation_espumantes",
            "dag_vitbrasil_extract_importation_suco_uva",
            "dag_vitbrasil_extract_importation_uvas_frescas",
            "dag_vitbrasil_extract_importation_uvas_passas",
            "dag_vitbrasil_extract_importation_vinhos_mesa",
            "dag_vitbrasil_extract_process_americanas_hibridas",
            "dag_vitbrasil_extract_process_uvas_mesa",
            "dag_vitbrasil_extract_process_viniferas",
            "dag_vitbrasil_extract_production"
        ]
    }
    ```

    **Notas:**
    - **`AIRFLOW_API_URL`**: URL da API do Airflow que fornece as informações sobre as DAGs.
    - **`AUTH`**: Credenciais para autenticação na API do Airflow.

    **Erros Possíveis:**

    - `401 Unauthorized`: O perfil do usuário não é `ADMIN`.
    - `500 Internal Server Error`: Problemas ao acessar a API do Airflow ou erros inesperados no servidor.
    """
    
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
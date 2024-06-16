# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

# =============================================================================
# CONSTANTES
# =============================================================================

PATH_DADOS_CATEGORIAS = {
    "comercializacao": "data/bronze/Comercio.csv",
    "exportacao": "data/bronze/ExpVinho.csv",
    "importacao": "data/bronze/ImpVinhos.csv",
    "producao": "data/bronze/Producao.csv",
    "processamento": "data/bronze/ProcessaViniferas.csv",
}

# =============================================================================
# CLASSES
# =============================================================================

# FUTURAS CLASSES DO PYDANTIC PARA VALIDAÇÃO DE DADOS

# =============================================================================
# FUNÇÕES
# =============================================================================

# FUTURAS FUNÇÕES

# =============================================================================
# CÓDIGO
# =============================================================================

# -----------------------------------------------------------------------------
# Aplicação
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------


@app.get("/dados/{categoria}")
async def get_dados(categoria: str) -> FileResponse:
    path_dado = PATH_DADOS_CATEGORIAS.get(categoria, None)
    if path_dado is None:
        raise HTTPException(
            status_code=404,
            detail=f"Arquivo não encontrado! Dados disponíveis: {', '.join(PATH_DADOS_CATEGORIAS.keys())}",
        )
    return FileResponse(path=path_dado, status_code=200)

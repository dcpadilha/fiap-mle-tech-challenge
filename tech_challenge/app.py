# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from tech_challenge.download_dados_csv import importa_endpoints_dados

# =============================================================================
# CÓDIGO
# =============================================================================

# -----------------------------------------------------------------------------
# Endpoints com os dados
# -----------------------------------------------------------------------------

ENDPOINTS_DADOS = importa_endpoints_dados()

# -----------------------------------------------------------------------------
# Aplicação
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------


@app.get("/dados/{categoria}")
@app.get("/dados/{categoria}/{subcategoria}")
async def get_dados(
    categoria: str, subcategoria: Optional[str] = None
) -> FileResponse:
    path_csv = (
        ENDPOINTS_DADOS.get(f"{categoria}/{subcategoria}")
        if subcategoria
        else ENDPOINTS_DADOS.get(f"{categoria}")
    )
    if path_csv is None:
        raise HTTPException(
            status_code=404,
            detail=f"Endpoint não existente! Os dados estão disponíveis nos endpoints: {', '.join(ENDPOINTS_DADOS.keys())}",
        )
    return FileResponse(path=path_csv, status_code=200)

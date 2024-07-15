# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel

# =============================================================================
# SCHEMAS
# =============================================================================


class Dados(BaseModel):
    categoria: str
    subCategoria: Optional[str] = None
    url: str
    pathDownload: Optional[Union[str, Path]] = None

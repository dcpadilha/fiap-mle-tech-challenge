# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import re
import unicodedata
from pathlib import Path
from typing import Optional

# =============================================================================
# CONSTANTES
# =============================================================================

NOME_PROJETO = "fiap-mle-tech-challenge"

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Retorna o caminho absoluto do diretório do projeto
# -----------------------------------------------------------------------------


def get_path_projeto(nome_projeto: str = NOME_PROJETO) -> str:
    """
    Retorna o caminho absoluto do diretório do projeto, subindo na estrutura de diretórios até encontrar o diretório com o nome do projeto especificado.

    Retorna:
    - caminho_projeto (str): Caminho absoluto do diretório do projeto.
    """

    path_atual = Path.cwd()

    # Subindo na estrutura de diretórios até encontrar o diretório do projeto
    while not str(path_atual.absolute()).endswith(nome_projeto):
        path_atual = path_atual.parent

    return str(path_atual.absolute())


# -----------------------------------------------------------------------------
# Normaliza uma string
# -----------------------------------------------------------------------------


def normaliza_str(input_str: Optional[str]) -> Optional[str]:
    """
    Remove todos os caracteres especiais e acentos das letras, retornando uma string com apenas letras.

    Parameters:
    - input_str (str): Texto a ser tratado
    - minuscula (bool): Se é para deixar tudo minúsculo ou não

    Returns:
    - str: Texto tratado com apenas letras
    """
    if input_str is None:
        return None
    # Importando as bibliotecas necessárias
    input_str = str(input_str)

    # Normalizando o texto conforme a forma NFC
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    output_str = "".join([
        c for c in nfkd_form if not unicodedata.combining(c)
    ])

    # Removendo as possíveis tags de HTML
    regex_tags = r"</?.>"
    output_str = re.sub(regex_tags, "", output_str)

    # Substituindo os caracteres especiais e números (tudo o que NÃO estiver de A-z)
    regex = re.compile(r"[^a-zA-Z\s]+")

    tokens = regex.sub(" ", output_str).split()

    # Deixando em minúscula
    tokens = list(map(lambda x: x.lower(), tokens))

    # Removendo possíveis espaços em branco no início e/ou fim da string
    output_str = (
        " ".join(map(lambda x: x.strip(), tokens)).strip().replace(" ", "_")
    )

    assert output_str, "normaliza_str: ERRO! output_str = ''"

    return output_str

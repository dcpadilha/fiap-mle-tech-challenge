# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from pathlib import Path

# =============================================================================
# CONSTANTES
# =============================================================================

NOME_PROJETO = "fiap-mle-tech-challenge"

# =============================================================================
# FUNÇÕES
# =============================================================================


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

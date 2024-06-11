def get_path_projeto() -> str:
    """
    Retorna o caminho absoluto do diretório do projeto, subindo na estrutura de diretórios até encontrar o diretório com o nome do projeto especificado.

    Retorna:
    - caminho_projeto (str): Caminho absoluto do diretório do projeto.
    """
    from pathlib import Path

    nome_projeto = "tech-challenge-1"
    path_atual = Path.cwd()

    # Subindo na estrutura de diretórios até encontrar o diretório do projeto
    while not str(path_atual.absolute()).endswith(nome_projeto):
        path_atual = path_atual.parent

    return str(path_atual.absolute())

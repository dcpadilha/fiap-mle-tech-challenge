# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from tech_challenge.schemas import Dados

# =============================================================================
# CONSTANTES
# =============================================================================

URL_RAIZ = "http://vitibrasil.cnpuv.embrapa.br/"

DADOS = [
    Dados(
        categoria="Produção",
        url=f"{URL_RAIZ}index.php?opcao=opt_02",
    ),
    Dados(
        categoria="Processamento",
        subCategoria="Viníferas",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_01",
    ),
    Dados(
        categoria="Processamento",
        subCategoria="Americanas e híbridas",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_02",
    ),
    Dados(
        categoria="Processamento",
        subCategoria="Uvas de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_03",
    ),
    Dados(
        categoria="Processamento",
        subCategoria="Sem classificação",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_04",
    ),
    Dados(
        categoria="Comercialização",
        url=f"{URL_RAIZ}index.php?opcao=opt_04",
    ),
    Dados(
        categoria="Importação",
        subCategoria="Vinhos de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_01",
    ),
    Dados(
        categoria="Importação",
        subCategoria="Espumantes",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_02",
    ),
    Dados(
        categoria="Importação",
        subCategoria="Uvas frescas",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_03",
    ),
    Dados(
        categoria="Importação",
        subCategoria="Uvas passas",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_04",
    ),
    Dados(
        categoria="Importação",
        subCategoria="Suco de uva",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_05",
    ),
    Dados(
        categoria="Exportação",
        subCategoria="Vinhos de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_01",
    ),
    Dados(
        categoria="Exportação",
        subCategoria="Espumantes",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_02",
    ),
    Dados(
        categoria="Exportação",
        subCategoria="Uvas frescas",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_03",
    ),
    Dados(
        categoria="Exportação",
        subCategoria="Suco de uva",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_04",
    ),
]

# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from pathlib import Path
from typing import Generator, List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from tech_challenge.utils import get_path_projeto


class Url(BaseModel):
    abaPrincipal: str
    abaSecundaria: str | None
    url: str


# =============================================================================
# CONSTANTES
# =============================================================================

URL_RAIZ = "http://vitibrasil.cnpuv.embrapa.br/"

urls = [
    Url(
        abaPrincipal="Produção",
        abaSecundaria=None,
        url=f"{URL_RAIZ}index.php?opcao=opt_02",
    ),
    Url(
        abaPrincipal="Processamento",
        abaSecundaria="Viníferas",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_01",
    ),
    Url(
        abaPrincipal="Processamento",
        abaSecundaria="Americanas e híbridas",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_02",
    ),
    Url(
        abaPrincipal="Processamento",
        abaSecundaria="Uvas de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_03",
    ),
    Url(
        abaPrincipal="Processamento",
        abaSecundaria="Sem classificação",
        url=f"{URL_RAIZ}index.php?opcao=opt_03&subopcao=subopt_04",
    ),
    Url(
        abaPrincipal="Comercialização",
        abaSecundaria=None,
        url=f"{URL_RAIZ}index.php?opcao=opt_04",
    ),
    Url(
        abaPrincipal="Importação",
        abaSecundaria="Vinhos de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_01",
    ),
    Url(
        abaPrincipal="Importação",
        abaSecundaria="Espumantes",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_02",
    ),
    Url(
        abaPrincipal="Importação",
        abaSecundaria="Uvas frescas",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_03",
    ),
    Url(
        abaPrincipal="Importação",
        abaSecundaria="Uvas passas",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_04",
    ),
    Url(
        abaPrincipal="Importação",
        abaSecundaria="Suco de uva",
        url=f"{URL_RAIZ}index.php?opcao=opt_05&subopcao=subopt_05",
    ),
    Url(
        abaPrincipal="Exportação",
        abaSecundaria="Vinhos de mesa",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_01",
    ),
    Url(
        abaPrincipal="Exportação",
        abaSecundaria="Espumantes",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_02",
    ),
    Url(
        abaPrincipal="Exportação",
        abaSecundaria="Uvas frescas",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_03",
    ),
    Url(
        abaPrincipal="Exportação",
        abaSecundaria="Suco de uva",
        url=f"{URL_RAIZ}index.php?opcao=opt_06&subopcao=subopt_04",
    ),
]


# =============================================================================
# FUNÇÕES
# =============================================================================


def get_links_download(urls: List[Url]) -> Generator:
    for url in urls:
        texto = (
            f"{url.abaPrincipal}"
            if url.abaSecundaria is None
            else f"{url.abaPrincipal} | {url.abaSecundaria}"
        )
        print(f"### {texto} ###\n> 🔗 Obtendo URL de download . . .")
        resposta = requests.get(url=url.url)
        html_da_pagina = resposta.content

        soup = BeautifulSoup(html_da_pagina, features="html.parser")

        def csv_href(href: str) -> bool:
            return href is not None and ".csv" in href

        resultados = soup.find_all(name="a", href=csv_href)
        if len(resultados) == 0:
            raise ValueError("💀 O link de download NÃO foi encontrado!")
        href_download = f"{URL_RAIZ}{resultados[0]["href"]}"

        print("> ✅ URL obtido!")

        yield texto, href_download


def faz_download(links: Generator) -> None:
    DIR_PROJETO = Path(get_path_projeto())
    dir_download = DIR_PROJETO / "data/bronze"
    dir_download.mkdir(exist_ok=True, parents=True)

    for texto, link_download in links:
        print(f"> 🕒 {texto}: Fazendo download . . .")

        nome_arquivo = link_download.split("/")[-1]
        path_download = dir_download / nome_arquivo

        if path_download.exists():
            print(f"> ❗ Arquivo '{path_download.name}' já existente!\n")
            continue

        with open(path_download, "wb") as arquivo_download:
            resposta = requests.get(link_download)
            arquivo_download.write(resposta.content)

        print("> ✅ Download feito!\n")

    return None


# =============================================================================
# CÓDIGO
# =============================================================================


def main() -> None:
    faz_download(get_links_download(urls))
    return None


if __name__ == "__main__":
    main()

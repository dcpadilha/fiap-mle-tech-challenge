# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import pickle
from pathlib import Path
from typing import Dict, Generator, List, Union

import requests
from bs4 import BeautifulSoup

from tech_challenge.common import DADOS, URL_RAIZ
from tech_challenge.schemas import Dados
from tech_challenge.utils import get_path_projeto, normaliza_str

# =============================================================================
# CONSTANTES
# =============================================================================

DIR_PROJETO = Path(get_path_projeto())
CAMADA_BRONZE = DIR_PROJETO / "data/bronze"
CAMADA_BRONZE.mkdir(exist_ok=True, parents=True)

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Representação em str dos dados
# -----------------------------------------------------------------------------


def texto_dados(dados: Dados) -> str:
    texto = (
        f"{dados.categoria}"
        if dados.subCategoria is None
        else f"{dados.categoria} | {dados.subCategoria}"
    )
    return texto


# -----------------------------------------------------------------------------
# Obtendo o link de download a partir da página web
# -----------------------------------------------------------------------------


def get_links_download(urls: List[Dados]) -> Generator:
    for url in urls:
        print(
            f"### {texto_dados(url)} ###\n> 🔗 Obtendo URL de download . . ."
        )
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

        yield url, href_download


# -----------------------------------------------------------------------------
# Salvando os dados com path de download <- facilitar endpoints
# -----------------------------------------------------------------------------


def exporta_endpoints_dados(endpoints: Dict[str, Union[str, Path]]) -> None:
    path_arquivo = CAMADA_BRONZE / "endpoints.pkl"

    with open(path_arquivo, "wb") as pkl_f:
        pickle.dump(obj=endpoints, file=pkl_f)

    return None


# -----------------------------------------------------------------------------
# Importando os dados com path de download <- facilitar endpoints
# -----------------------------------------------------------------------------


def importa_endpoints_dados() -> Dict[str, Union[str, Path]]:
    path_arquivo = CAMADA_BRONZE / "endpoints.pkl"

    if not path_arquivo.exists():
        raise FileNotFoundError(
            "importa_dados_com_path: ERRO! Os dados não foram baixados para o servidor!"
        )

    with open(path_arquivo, "rb") as pkl_f:
        endpoints = pickle.load(file=pkl_f)

    return endpoints


# -----------------------------------------------------------------------------
# Fazendo download dos arquivos
# -----------------------------------------------------------------------------


def faz_download(links: Generator) -> None:
    endpoints = {}

    for url, link_download in links:
        print(f"> 🕒 {texto_dados(url)}: Fazendo download . . .")

        nome_arquivo = link_download.split("/")[-1]
        path_download = CAMADA_BRONZE / nome_arquivo

        url.pathDownload = path_download
        endpoint = (
            f"{normaliza_str(url.categoria)}/{normaliza_str(url.subCategoria)}"
            if url.subCategoria
            else f"{normaliza_str(url.categoria)}"
        )
        endpoints[endpoint] = path_download

        if path_download.exists():
            print(f"> ❗ Arquivo '{path_download.name}' já existente!\n")
            continue

        with open(path_download, "wb") as arquivo_download:
            resposta = requests.get(link_download)
            arquivo_download.write(resposta.content)

        print("> ✅ Download feito!\n")

    exporta_endpoints_dados(endpoints)

    return None


# =============================================================================
# CÓDIGO
# =============================================================================


def main() -> None:
    faz_download(get_links_download(DADOS))
    return None


if __name__ == "__main__":
    main()

from typing import Dict, Generator
from bs4 import BeautifulSoup
import requests

URL_RAIZ = "http://vitibrasil.cnpuv.embrapa.br/"

urls = {
    "Produção": f"{URL_RAIZ}index.php?opcao=opt_02",
    "Processamento": f"{URL_RAIZ}index.php?opcao=opt_03",
    "Comercialização": f"{URL_RAIZ}index.php?opcao=opt_04",
    "Importação": f"{URL_RAIZ}index.php?opcao=opt_05",
    "Exportação": f"{URL_RAIZ}index.php?opcao=opt_06",
}


def get_links_download(urls: Dict[str, str]) -> Generator:
    for aba, link_aba in urls.items():
        print(f"### {aba} ###\n> Obtendo URL de download . . .")
        resposta = requests.get(url=link_aba)
        html_da_pagina = resposta.content

        soup = BeautifulSoup(html_da_pagina, features="html.parser")

        def csv_href(href: str) -> bool:
            return href is not None and ".csv" in href

        resultados = soup.find_all(name="a", href=csv_href)
        if len(resultados) == 0:
            raise ValueError("O link de download NÃO foi encontrado!")
        href_download = f"{URL_RAIZ}{resultados[0]["href"]}"

        print("> URL obtido!")

        yield aba, href_download


def faz_download(links: Generator) -> None:
    from pathlib import Path
    from utils import get_path_projeto

    DIR_PROJETO = Path(get_path_projeto())
    dir_download = DIR_PROJETO / "data/bronze"
    dir_download.mkdir(exist_ok=True, parents=True)

    for _, link_download in links:
        print(f"> Fazendo download . . .")

        nome_arquivo = link_download.split("/")[-1]

        with open(dir_download / nome_arquivo, "wb") as arquivo_download:
            resposta = requests.get(link_download)
            arquivo_download.write(resposta.content)

        print("> Download feito!\n")

    return None


faz_download(get_links_download(urls))

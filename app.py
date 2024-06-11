
import requests
from bs4 import BeautifulSoup as bts
import pandas as pd
import re
import time
import datetime
import socket
from fastapi import FastAPI, Request

TIMEOUT_SEC = 10 # default timeout in seconds
socket.setdefaulttimeout(TIMEOUT_SEC)

def getAndParseURL(url):
    result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = bts(result.text, 'html.parser')
    return soup

app = FastAPI()

main_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01"
base_url = 'http://vitibrasil.cnpuv.embrapa.br/download/'

files = {'file_dot_comma': ['Producao.csv',
        'ProcessaViniferas.csv',
        'Comercio.csv',
        'ImpVinhos.csv',
        'ImpEspumantes.csv',
        'ImpFrescas.csv',
        'ImpPassas.csv',
        'ImpSuco.csv',
        'ExpVinho.csv',
        'ExpEspumantes.csv',
        'ExpUva.csv',
        'ExpSuco.csv'],
        'file_t': ['ProcessaAmericanas.csv',
        'ProcessaMesa.csv'] }

file_sep = {
    'file_dot_comma': ';',
    'file_t': '\t'
}

html_footer = getAndParseURL(main_url).find_all("table", {"class": "tb_base tb_footer"})
bs_text_tag = html_footer[0].select('td')[0]
last_date_regex = r"Última modificação: (\d{2})/(\d{2})/(\d{2})"
match = re.search(last_date_regex, bs_text_tag.get_text())

if match:
    day, month, year = match.groups()
    modified_date = datetime.datetime(year=int(year)+2000, month=int(month), day=int(day))
    print("Última modificação:", modified_date.strftime("%d-%m-%Y"))
else:
    print("Não foi possível encontrar a data da 'Última modificação' do site")

dataframes = []
for file_type, filenames in files.items():
    for filename in filenames:
        try:
            df = pd.read_csv(base_url + filename, sep=file_sep[file_type])
            dataframes.append(df)
        except Exception as e:
            df = pd.DataFrame()  
            dataframes.append(df)
            print(f"Error reading {filename}: {e}")

df_dict = {
    'Producao': dataframes[0],
    'ProcessaViniferas': dataframes[1],
    'ProcessaAmericanas': dataframes[2],
    'ProcessaMesa': dataframes[3],
    'Comercio': dataframes[4],
    'ImpVinhos': dataframes[5],
    'ImpEspumantes': dataframes[6],
    'ImpFrescas': dataframes[7],
    'ImpPassas': dataframes[8],
    'ImpSuco': dataframes[9],
    'ExpVinho': dataframes[10],
    'ExpEspumantes': dataframes[11],
    'ExpUva': dataframes[12],
    'ExpSuco': dataframes[13]
}


@app.get("/dados-csv")
async def get_csv_data(request: Request):
    """
    Rota para fornecer dados de um arquivo CSV.

    Parâmetros:
        request: Objeto de solicitação do FastAPI.

    Retorno:
        Dicionário contendo os dados do CSV.
    """

    # Obter o nome do arquivo CSV a partir da solicitação
    file_name = request.query_params["file_name"]

    # Ler o arquivo CSV e converter em DataFrame
    try:
        data = pd.read_csv(file_name)
    except FileNotFoundError:
        return {"mensagem": f"Arquivo CSV '{file_name}' não encontrado."}, 404

    # Converter DataFrame em dicionário
    data_dict = data.to_dict(orient="records")

    return data_dict
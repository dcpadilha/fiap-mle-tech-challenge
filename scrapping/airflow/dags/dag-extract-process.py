from airflow.decorators import dag, task
import pendulum
from bs4 import BeautifulSoup
import requests

import json
import utils
from enum import Enum
import os

from airflow.macros import ds_add


@dag(
    schedule = "@yearly",
    start_date = pendulum.datetime(1970, 1, 1, tz="UTC"),
    catchup = True,
)
def dag_vitbrasil_extract_process():

    data = []

    @task()
    def run_scrapping(ds = None, ds_nodash = None):

        base_url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ds[:4]}opcao=opt_02"
        html_page = requests.get(base_url).text
        soup = BeautifulSoup(html_page, "html.parser")

        tables = soup.find_all('table', class_='tb_base tb_dados')

        for table in tables:
            rows = table.find_all('tr')

            current_item = None
            for row in rows:
                main_cell = row.find('td', class_='tb_item')
                if main_cell:                    
                    # Se encontrar um item principal, inicializa o dicionário
                    item_name = utils.remove_space(main_cell.text)
                   
                    current_item = {item_name: {"Ano da Informação": ds[:4]}}
                    # print(current_item)
                    data.append(current_item)
                else:
                    # Se não for item principal, processa como subitem
                    sub_cells = row.find_all('td')
                    if sub_cells and len(sub_cells) > 1:

                        sub_item_name = utils.remove_space(sub_cells[0].text)
                        
                        if not 'Total' in sub_item_name:
                            sub_item_value = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", "")) 
                            current_item[item_name][sub_item_name] = sub_item_value

    @task()
    def save_json(ds = None, ds_nodash = None):

        directory = f"./data/Production/"
        filename = f"Production_{ds[:4]}.json"
        filepath = os.path.join(directory, filename)

        # Garantir que o diretório existe
        os.makedirs(directory, exist_ok=True)

        with open(f"{filepath}", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4,  ensure_ascii=False)
        
            print(f"salvou em: {filepath}")
        

    run_scrapping()
    save_json()
            
dag_vitbrasil_extract_process()


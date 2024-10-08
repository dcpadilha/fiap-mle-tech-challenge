from airflow.decorators import dag, task
import pendulum
from bs4 import BeautifulSoup
import requests
from datetime import timedelta

import utils

@dag(
    schedule = "@yearly",
    start_date = pendulum.datetime(1970, 1, 1, tz="UTC"),
    catchup = True,
    default_args = {"retries": 1, "retry_delay": timedelta(minutes=3)}
)
def dag_vitbrasil_extract_process_americanas_hibridas():

    @task()
    def run_scrapping(ds = None, ds_nodash = None, **kwargs):

        data = []

        year = kwargs["dag_run"].conf.get("year_reprocess")

        if year == None:
            year = ds[:4]

        utils.delete_data("Processamento", "Americanas e Hibridas", year)


        base_url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_02"  
        html_page = requests.get(base_url).text
        soup = BeautifulSoup(html_page, "html.parser")

        tables = soup.find_all("table", class_="tb_base tb_dados")
        
        for table in tables:
            rows = table.find_all("tr")

            current_item = None
            for row in rows:
                main_cell = row.find("td", class_="tb_item")
                if main_cell:                    
                    # Se encontrar um item principal, inicializa o dicionário
                    item_name = utils.remove_space(main_cell.text)
                   
                    current_item = {item_name: {"Ano da Informação": year}}
                    # print(current_item)
                    data.append(current_item)
                else:
                    # Se não for item principal, processa como subitem
                    sub_cells = row.find_all("td")
                    if sub_cells and len(sub_cells) > 1:

                        sub_item_name = utils.remove_space(sub_cells[0].text)
                        
                        if not "Total" in sub_item_name and not "Sem classificação" in sub_item_name:
                            sub_item_value = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", "")) 
                            current_item[item_name][sub_item_name] = sub_item_value
        
        kwargs["ti"].xcom_push(key="dados", value=data)

    @task()
    def save_on_database(**kwargs):
        utils.save_database(kwargs["ti"].xcom_pull(key="dados"), "Processamento", "Americanas e Hibridas")

    run_scrapping() >> save_on_database()
    
dag_vitbrasil_extract_process_americanas_hibridas()
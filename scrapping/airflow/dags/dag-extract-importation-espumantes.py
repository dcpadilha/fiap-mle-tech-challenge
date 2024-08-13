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
def dag_vitbrasil_extract_importation_espumantes():

    @task()
    def run_scrapping(ds = None, ds_nodash = None, **kwargs):

        data = []

        year = kwargs["dag_run"].conf.get("year_reprocess")

        if year == None:
            year = ds[:4]
        
        utils.delete_data("Importacao", "Espumantes", year)

        base_url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_02"  
        html_page = requests.get(base_url).text
        soup = BeautifulSoup(html_page, "html.parser")

        tables = soup.find_all("table", class_="tb_base tb_dados")
        
        for table in tables:
            rows = table.find_all('tr')
            current_item = None
            for row in rows:
                sub_cells = row.find_all('td')
                if sub_cells and len(sub_cells) > 1:
                    item_name = utils.remove_space(sub_cells[0].text)

                    current_item = {item_name: {"Ano da Informação": year}}
                    if not "Total" in item_name and not "Sem classificação" in item_name:
                        data.append(current_item)
                        sub_item_qtde = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", ""))
                        sub_item_value = utils.convert_to_int(sub_cells[2].text.replace(" ", "").replace("\n","").replace(".", ""))

                        current_item[item_name]["quantidade"] = sub_item_qtde
                        current_item[item_name]["valor"] = sub_item_value
        
        kwargs["ti"].xcom_push(key="dados", value=data)

    @task()
    def save_on_database(**kwargs):
        utils.save_database_value_and_qtde(kwargs["ti"].xcom_pull(key="dados"), "Importacao", "Espumantes")

    run_scrapping() >> save_on_database()
    
dag_vitbrasil_extract_importation_espumantes()
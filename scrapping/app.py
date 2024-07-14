from bs4 import BeautifulSoup
import requests

import json
import utils
from enum import Enum
import os

class TypeOption(Enum):
    Production = {"item": "opt_02"}

    Proccess = {"item": "opt_03", "subitens": [["subopt_01", "subopt_02", "subopt_03", "subopt_04"]]}
    Commercialization = {"item": "opt_04", "subitens": [["subopt_01", "subopt_02", "subopt_03", "subopt_04"]]}
    Importation = {"item": "opt_05", "subitens": [["subopt_01", "subopt_02", "subopt_03", "subopt_04"]]}
    Exportation = {"item": "opt_06", "subitens": [["subopt_01", "subopt_02", "subopt_03", "subopt_04"]]}


class ScrappingApp():

    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.soup = None
        self.html_page = None
        self.data = []

    def get_base_html(self):
        self.html_page = requests.get(f"{self.base_url}?opcao={TypeOption.Production.value}").text
        self.soup = BeautifulSoup(self.html_page, "html.parser")

    def get_years_of_data(self):
        # Responsável por coletar o range de datas
        tb_datas = self.soup.find_all("table")[5]
        str_datas = tb_datas.find("label", attrs={"class": "lbl_pesq"}).text

        return utils.transform_data_list(str_datas)

        
    def get_info_page(self):
        tables = self.soup.find_all('table', class_='tb_base tb_dados')

        for table in tables:
            rows = table.find_all('tr')

            current_item = None
            for row in rows:
                main_cell = row.find('td', class_='tb_item')
                if main_cell:                    
                    # Se encontrar um item principal, inicializa o dicionário
                    item_name = utils.remove_space(main_cell.text)
                    item_value = utils.convert_to_int(utils.remove_space(main_cell.find_next_sibling('td').text))
                    current_item = {item_name: {"Valor Total": item_value, "Ano da Informação": "2024"}}
                    # print(current_item)
                    self.data.append(current_item)
                else:
                    # Se não for item principal, processa como subitem
                    sub_cells = row.find_all('td')
                    if sub_cells and len(sub_cells) > 1:

                        sub_item_name = utils.remove_space(sub_cells[0].text)
                        
                        if not 'Total' in sub_item_name:
                            sub_item_value = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", "")) 
                            current_item[item_name][sub_item_name] = sub_item_value
        self.save_json("data", "Production", "")

    def save_json(self, filename: str, name_page: str, actual_year: str):

        directory = f"./data/{name_page}/"
        filename = f"{name_page}_{filename}_actual_year.json"
        filepath = os.path.join(directory, filename)

        # Garantir que o diretório existe
        os.makedirs(directory, exist_ok=True)

        with open(f"{filepath}", "w", encoding="utf-8") as json_file:
            json.dump(self.data, json_file, indent=4,  ensure_ascii=False)

    def run(self):
        self.get_base_html()
        self.get_years_of_data()
        self.get_info_page()
        


if __name__ == '__main__':
    ScrappingApp().run()

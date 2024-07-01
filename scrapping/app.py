from bs4 import BeautifulSoup
import requests
import re
import json
import utils
from enum import Enum
import os

class TypeOption(Enum):
    Production = "opt_02"
    Proccess = "opt_03"
    Commercialization = "opt_04"
    Importation = "opt_05"
    Exportation = "opt_06"


class ScrappingApp():

    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.soup = None
        self.html_page = None
        self.data = None

    def get_base_html(self):
        self.html_page = requests.get(f"{self.base_url}?opcao={TypeOption.Production.value}").text
        self.soup = BeautifulSoup(self.base_url, "html.parser")

    def get_years_of_data(self):
        # Responsável por coletar o range de datas
        tb_datas = self.soup.find_all("table")[5]
        str_datas = tb_datas.find("label", attrs={"class": "lbl_pesq"}).text
        pattern = r'\[\s*(\d{4})\s*-\s*(\d{4})\s*\]'
        match = re.search(pattern, str_datas)

        return list(range(int(match.group(1)), (int(match.group(2) + 1))))
        
    def get_info_page(self):
        tables = self.soup.find_all('table', class_='tb_base tb_dados')

        for table in tables:
            rows = table.find_all('tr')
            
            current_item = None
            for row in rows:
                main_cell = row.find('td', class_='tb_item')
                if main_cell:
                    item_name =  re.sub(r'^\s+|\s+$', '', main_cell.text)
                    
                    # Se encontrar um item principal, inicializa o dicionário
                    item_name = main_cell.text
                    item_name =  re.sub(r'^\s+|\s+$', '', main_cell.text)
                    
                    item_value = utils.convert_to_int(main_cell.find_next_sibling('td').text)

                    current_item = {item_name: {"Valor Total": item_value, "Ano da Informação": '2024'}}
                    self.data.append(current_item)
                else:
                    # Se não for item principal, processa como subitem
                    sub_cells = row.find_all('td')
                    if sub_cells and len(sub_cells) > 1:

                        sub_item_name = re.sub(r'^\s+|\s+$', '', sub_cells[0].text)
                        if not 'Total' in sub_item_name:
                            sub_item_value = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", "")) 
                            current_item[item_name][sub_item_name] = sub_item_value
        self.save_json("data", "Production")

    def save_json(self, filename: str, name_page: str):

        directory = './data'
        filename = f'{filename}.json'
        filepath = os.path.join(directory, filename)

        # Garantir que o diretório existe
        os.makedirs(directory, exist_ok=True)

        with open(f'{filepath}', 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, indent=4,  ensure_ascii=False)

    def run(self):
        self.get_base_html()
        self.get_info_page()
        self.get_years_of_data()
        


if __name__ == '__main__':
    ScrappingApp().run()

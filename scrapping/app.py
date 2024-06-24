from bs4 import BeautifulSoup
import requests
import re
import json
import utils

Production = "opt_02"
Proccess = "opt_03"
Commercialization = "opt_04"
Importation = "opt_05"
Exportation = "opt_06"

base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"

html_page = requests.get(f"{base_url}?opcao={Production}").text
soup = BeautifulSoup(html_page, "html.parser")

tb_datas = soup.find_all("table")[5]
str_datas = tb_datas.find("label", attrs={"class": "lbl_pesq"}).text
pattern = r'\[\s*(\d{4})\s*-\s*(\d{4})\s*\]'
match = re.search(pattern, str_datas)

start_date, end_date = int(match.group(1)), int(match.group(2))

print(start_date, end_date)

tables = soup.find_all('table', class_='tb_base tb_dados')


list_years = list(range(start_date, (end_date + 1)))

data = []

    
current_year = start_date


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

            current_item = {item_name: {"Valor Total": item_value, "Ano da Informação": current_year}}
            data.append(current_item)
        else:
            # Se não for item principal, processa como subitem
            sub_cells = row.find_all('td')
            if sub_cells and len(sub_cells) > 1:

                sub_item_name = re.sub(r'^\s+|\s+$', '', sub_cells[0].text)
                if not 'Total' in sub_item_name:
                    sub_item_value = utils.convert_to_int(sub_cells[1].text.replace(" ", "").replace("\n","").replace(".", "")) 
                    current_item[item_name][sub_item_name] = sub_item_value

with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4,  ensure_ascii=False)

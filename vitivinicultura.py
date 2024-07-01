import requests
from bs4 import BeautifulSoup as bts
import pandas as pd
import re
import datetime

class Vitivinicultura():
    def __init__(self):
        self.url_date = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01'
        self.base_url = 'http://vitibrasil.cnpuv.embrapa.br/download/'
        self.path_files = 'data_vitivinicultura/csv/'

        self.files = {'file_dot_comma': ['Producao.csv',
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

        self.file_sep = {
                        'file_dot_comma': ';',
                        'file_t': '\t'
                    }

        self.dataframes = []

    def getAndParseURL(self, url):
        result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
        soup = bts(result.text, 'html.parser')
        return soup
    
    def get_last_updated_date(self,):

        html = self.getAndParseURL(self.url_date)
        html_footer = html.find_all("table", {"class": "tb_base tb_footer"})
        bs_text_tag = html_footer[0].select('td')[0]
        modification_date_regex = r"Última modificação: (\d{2})/(\d{2})/(\d{2})"
        match = re.search(modification_date_regex, bs_text_tag.get_text())

        if match:
            day, month, year = match.groups()
            modified_date = datetime.datetime(year=int(year)+2000, month=int(month), day=int(day))

            print("Última modificação:", modified_date.strftime("%d-%m-%Y"))
            return modified_date.date()
        else:
            print("Não foi possível encontrar a data da 'Última modificação' do site")
            return datetime.date(2023,12,21)

    def load_data(self, path):
        for file_type, filenames in self.files.items():
            for filename in filenames:
                try:
                    df = pd.read_csv(path + filename, sep=self.file_sep[file_type])
                    self.dataframes.append(df)
                except Exception as e:
                    df = pd.DataFrame()  
                    self.dataframes.append(df)
                    print(f"Error reading {filename}: {e}")
        return self.dataframes
    
    def get_df_dict(self,modified_date, ultima_data_coletada):
        if modified_date > ultima_data_coletada:
            print('Coletando dados via scraping...')
            dataframes = self.load_data(self.base_url)
        else:
            print('Lendo dados do localmente...')
            dataframes = self.load_data(self.path_files)
        self.df_dict = {
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
        #return self.df_dict   
    
    def get_tabela_especifica(self,df_key: str):
        """
        Function to retrieve data based on the key
        """
        if df_key not in self.df_dict:
            print(f"Error: Dataframe '{df_key}' not found")
            return None
        else:
            return self.df_dict[df_key]
from bs4 import BeautifulSoup
import requests
import re






class AppScrapping():

    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"


    def get_base_html(self):
        self.base_html = requests.get(f"{self.base_url}?opcao=opt_02").text
        self.soup = BeautifulSoup(self.base_html, "html.parser")

    def get_years(self):
        tb_datas = self.soup.find_all("table")[5]
        str_datas = tb_datas.find("label", attrs={"class": "lbl_pesq"}).text
        pattern = r'\[\s*(\d{4})\s*-\s*(\d{4})\s*\]'
        match = re.search(pattern, str_datas)
        return match.group(1), match.group(2) 
    
    def generate_years_searching(self):

        start_year, end_year = get_years


app_scrapping = AppScrapping()

app_scrapping.get_base_html()

print(app_scrapping.get_years())
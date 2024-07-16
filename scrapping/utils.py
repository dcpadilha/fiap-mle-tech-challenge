import re
import pendulum
import mysql.connector
from mysql.connector import Error
import pandas as pd
import sys


def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
    
def remove_space(value: str):
    return re.sub(r'^\s+|\s+$', '',value)

def transform_data_list(value: str):

    pattern = r'\[\s*(\d{4})\s*-\s*(\d{4})\s*\]'
    match = re.search(pattern, value)

    start_year = int(match.group(1))
    end_year = int(match.group(2))

    return list(range(start_year, (end_year + 1)))


def get_db_conn():
    user = "root"
    password = "root"
    host = "172.20.10.4" 
    database = "tech_challenge"

    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )      

    return conn

def save_database(data, typeProduct: str):
    rows = []
    for item in data:
        for category, values in item.items():
            year = values.pop("Ano da Informação")
            for subtipo, valor in values.items():
                rows.append({
                    "ano": year,
                    "categoria": category,
                    "subcategoria": subtipo,
                    "valor": valor,
                    "inserted_at": pendulum.now(tz='America/Sao_Paulo')
                })

    df = pd.DataFrame(rows)

    try:
        conn = get_db_conn()

        if conn.is_connected():
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO vitibrasil (ano, origem, categoria, subcategoria, valor, inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            for _, row in df.iterrows():
                cursor.execute(insert_query, (row['ano'], typeProduct, row['categoria'], row['subcategoria'], row['valor'], row['inserted_at']))

            conn.commit()
        else:
            raise Exception("Conexão com o MySQL inexistente")

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        sys.exit(1)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
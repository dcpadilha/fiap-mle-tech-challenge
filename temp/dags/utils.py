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
    host = "mysql" 
    database = "tech_challenge"

    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )      

    return conn

def save_database(data, origem: str, suborigem: str):
    rows = []
    for item in data:
        for category, values in item.items():
            year = values.pop("Ano da Informação")
            for subtipo, valor in values.items():
                rows.append({
                    "ano": year,
                    "categoria": category,
                    "subcategoria": subtipo,
                    "qtde_kg": valor,
                    "inserted_at": pendulum.now(tz='America/Sao_Paulo')
                })

    df = pd.DataFrame(rows)

    try:
        conn = get_db_conn()

        if conn.is_connected():
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO vitibrasil (ano, origem, sub_origem, categoria, sub_categoria, qtde_kg, inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            for _, row in df.iterrows():
                cursor.execute(insert_query, (row['ano'], origem, suborigem, row['categoria'], row['subcategoria'], row['qtde_kg'], row['inserted_at']))

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

        
def save_database_value_and_qtde(data, origem: str, suborigem: str):
    rows = []
    for item in data:
        for category, values in item.items():
            rows.append({
              "ano": values.get("Ano da Informação"),
              "categoria": category,
              "subcategoria": "",
              "valor": values.get('valor'),
              "qtde_kg": values.get('quantidade'),
              "inserted_at": "2023-01-01"
          })

    df = pd.DataFrame(rows)

    try:
        conn = get_db_conn()

        if conn.is_connected():
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO vitibrasil (ano, origem, sub_origem, categoria, sub_categoria, qtde_kg, valor, inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            for _, row in df.iterrows():
                cursor.execute(insert_query, (row['ano'], origem, suborigem, row['categoria'], row['subcategoria'], row['qtde_kg'], row['valor'], row['inserted_at']))

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
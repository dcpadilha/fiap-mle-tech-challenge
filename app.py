import datetime
from fastapi import FastAPI,  HTTPException
from vitivinicultura import Vitivinicultura

app = FastAPI()
vt = Vitivinicultura()

modified_date = vt.get_last_updated_date()
ultima_data_coletada = datetime.date(2023,12,21)

vt.get_df_dict(modified_date, ultima_data_coletada)
df_dict = vt.df_dict

@app.get("/retorna_dados/")
async def get_data(df_key: str, year: int = None):
    """
    Function to retrieve data based on the key and optional year
    """
    try:
        if df_key not in df_dict:
            raise HTTPException(status_code=404, detail={"error": f"Dataframe '{df_key}' not found. Select one of this options {list(df_dict)}"}) 
        df = vt.get_tabela_especifica(df_key)
        if year:
            year = str(year)
            if year not in df.columns:
                raise HTTPException(status_code=404, detail= {"error": f"Year '{year}' not found in '{df_key}' data"})
            data = df[[f"produto", f"{year}"]].to_dict(orient="records")  # Improved column selection
        else:
            data = df.to_dict(orient="records")
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail={"error": f"Unexpected error: {e}"})  # Generic error message for unexpected issues

# @app.get("/dados-producao")
# async def get_producao(request: Request):
#     return df_dict['Producao'].to_dict(orient="records")

# @app.get("/dados-processaviniferas")
# async def get_processaviniferas(request: Request):
#     return df_dict['ProcessaViniferas'].to_dict(orient="records")

# @app.get("/dados-processaamericanas")
# async def get_processaamericanas(request: Request):
#     return df_dict['ProcessaAmericanas'].to_dict(orient="records")

# @app.get("/dados-processamesa")
# async def get_processamesa(request: Request):
#     return df_dict['ProcessaMesa'].to_dict(orient="records")

# @app.get("/dados-comercio")
# async def get_comercio(request: Request):
#     return df_dict['Comercio'].to_dict(orient="records")

# @app.get("/dados-impvinhos")
# async def get_impvinhos(request: Request):
#     return df_dict['ImpVinhos'].to_dict(orient="records")

# @app.get("/dados-impespumantes")
# async def get_impespumantes(request: Request):
#     return df_dict['ImpEspumantes'].to_dict(orient="records")

# @app.get("/dados-impfrescas")
# async def get_impfrescas(request: Request):
#     return df_dict['ImpFrescas'].to_dict(orient="records")

# @app.get("/dados-imppassas")
# async def get_imppassas(request: Request):
#     return df_dict['ImpPassas'].to_dict(orient="records")

# @app.get("/dados-impsuco")
# async def get_impsuco(request: Request):
#     return df_dict['ImpSuco'].to_dict(orient="records")

# @app.get("/dados-expvinho")
# async def get_expvinho(request: Request):
#     return df_dict['ExpVinho'].to_dict(orient="records")

# @app.get("/dados-expespumantes")
# async def get_expespumantes(request: Request):
#     return df_dict['ExpEspumantes'].to_dict(orient="records")

# @app.get("/dados-expuva")
# async def get_expuva(request: Request):
#     return df_dict['ExpUva'].to_dict(orient="records")

# @app.get("/dados-expsuco")
# async def get_expsuco(request: Request):
#     return df_dict['ExpSuco'].to_dict(orient="records")

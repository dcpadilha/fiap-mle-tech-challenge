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
            data = df[[f"produto", f"{year}"]].to_dict(orient="records")  
        else:
            data = df.to_dict(orient="records")
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail={"error": f"Unexpected error: {e}"})  

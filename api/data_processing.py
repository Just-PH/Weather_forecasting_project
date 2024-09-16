from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import uvicorn
app = FastAPI()

# Charger les données du CSV dans un DataFrame
df = pd.read_csv('./result/paris_hourly_data.csv')

@app.get("/data")
def get_data(start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    # Filtrer les données en fonction des paramètres de requête
    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    else:
        filtered_df = df

    # Convertir le DataFrame filtré en dictionnaire
    data = filtered_df.to_dict(orient='records')

    return data

if __name__ == '__main__':

    uvicorn.run(app, host="127.0.0.1", port=8000)
    dataframe=get_data(start_date='2021-09-10', end_date='2021-09-11')
    print(dataframe.head(2))

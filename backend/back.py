from fastapi import FastAPI
from backend.api.geocode import get_coordinates
from backend.api.open_meteo import get_temperature, get_history
from backend.model.LSTM_functions import fit_LSTM_model, predict_from_model, load_LSTM_model
import datetime
import pandas as pd
import numpy as np
import os
app = FastAPI()

# define a root '/' endpoint
@app.get("/")
def index():
    return {"message": "It works!"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}"}

@app.get("/temperature/{city}")
def temperature(city: str):
    """
    Retrieves the temperature for a given city.
    This function takes the name of a city, fetches its geographical coordinates,
    and then retrieves the current temperature for those coordinates. The temperature
    is added to the data dictionary and returned.
    Args:
        city (str): The name of the city for which to retrieve the temperature.
    Returns:
        dict: A dictionary containing the city's coordinates and temperature.
    """
    data = get_coordinates(city)
    temp = get_temperature(data['lat'], data['lng'])
    data['temperature'] = temp
    return data

@app.get("/predict_temperature/{city}")
def prediction(city: str):
    """
    Predicts the temperature for a given city using historical weather data and a pre-trained LSTM model.
    Args:
        city (str): The name of the city for which the temperature prediction is to be made.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the predicted temperatures for the next 24 hours.
            Each dictionary has the following keys:
                - 'date': The date and time of the prediction.
                - 'predicted_temperature': The predicted temperature rounded to one decimal place.
    """

    # get the coordinates of the city
    spatial_data = get_coordinates(city)
    # get the date of yesterday and previous week
    yesterday = datetime.datetime.now() - datetime.timedelta(days=2)
    yesterday = yesterday.strftime("%Y-%m-%d")
    previous_week = datetime.datetime.now() - datetime.timedelta(days=16)
    previous_week = previous_week.strftime("%Y-%m-%d")
    # get previous week data from the Open-Meteo API for the city
    history = get_history(spatial_data['lat'], spatial_data['lng'], previous_week, yesterday)
    df = pd.DataFrame({'date': history['time'], 'temperature': history['temperature_2m']})
    df['date'] = pd.to_datetime(df['date'])
    # Load model and scaler
    scaler_path = os.path.join(os.path.dirname(__file__), 'model','model_saved', 'saved_models_scaler.pkl')
    model_path = os.path.join(os.path.dirname(__file__), 'model','model_saved', 'saved_models.keras')
    model , scaler = load_LSTM_model(model_path,scaler_path)
    forecast = predict_from_model(df, model, scaler)
    forecast = forecast[-24:]
    forecast['predicted_temperature'] = forecast['predicted_temperature'].apply(lambda x: round(x, 1))
    return forecast.to_dict(orient="records")

from backend.api.geocode import get_coordinates
from backend.api.open_meteo import get_temperature, get_history
from backend.model.LSTM_functions import fit_LSTM_model, predict_from_model, load_LSTM_model, retrain_and_compare_LSTM
import datetime
import pandas as pd
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import threading


app = FastAPI()
SECRET_TOKEN = os.getenv("RETRAIN_TOKEN", "dev_token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root '/' endpoint
@app.get("/")
def index():
    """
    Root endpoint that checks if the server is running.

    Returns:
        dict: A message indicating the server is working.
    """
    return {"message": "It works!"}

@app.get("/hello/{name}")
def hello_name(name: str):
    """
    Endpoint that returns a greeting message for the provided name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        dict: A greeting message.
    """
    return {"message": f"Hello, {name}"}

@app.get("/temperature/{city}")
def temperature(city: str):
    """
    Retrieves the current temperature for a given city.
    This function fetches the geographical coordinates of the city,
    retrieves the current temperature for those coordinates, and returns the data.

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
def predict_temperature(city: str):
    """
    Predicts the temperature for a given city using historical weather data and a pre-trained LSTM model.

    Args:
        city (str): The name of the city for which the temperature prediction is to be made.

    Returns:
        dict: A dictionary of predicted temperatures for the next 24 hours.
              Each entry includes the 'date' and 'predicted_temperature'.
    """
    # Get the coordinates of the city
    spatial_data = get_coordinates(city)
    # Get the date of yesterday and the previous week
    yesterday = datetime.datetime.now() - datetime.timedelta(days=2)
    yesterday = yesterday.strftime("%Y-%m-%d")
    previous_week = datetime.datetime.now() - datetime.timedelta(days=16)
    previous_week = previous_week.strftime("%Y-%m-%d")

    # Get historical data from the Open-Meteo API for the city
    history = get_history(spatial_data['lat'], spatial_data['lng'], previous_week, yesterday)

    # Prepare data for prediction
    df = pd.DataFrame({'date': history['time'], 'temperature': history['temperature_2m']})
    df['date'] = pd.to_datetime(df['date'])

    # Load model and scaler
    scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'model_saved', 'saved_models_scaler.pkl')
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'model_saved', 'saved_models.keras')
    model, scaler = load_LSTM_model(model_path, scaler_path)

    # Predict the temperature
    forecast = predict_from_model(df, model, scaler)
    forecast = forecast[-24:]
    forecast['predicted_temperature'] = forecast['predicted_temperature'].apply(lambda x: round(x, 1))

    return forecast.set_index('date')['predicted_temperature'].to_dict()


security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "mon_token_ultra_secret":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

def run_training(city: str, model_name: str = None):
    try:
        spatial_data = get_coordinates(city)
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        start_date = "2010-01-01"

        history = get_history(spatial_data['lat'], spatial_data['lng'], start_date, yesterday)
        if not history:
            print("No historical data found.")
            return

        new_data = pd.DataFrame({'date': history['time'], 'temperature': history['temperature_2m']})
        new_data['date'] = pd.to_datetime(new_data['date'])

        model_path = os.path.join(os.path.dirname(__file__), 'model', 'model_saved', 'saved_models.keras')
        scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'model_saved', 'saved_models_scaler.pkl')

        _, _, _, model_updated = retrain_and_compare_LSTM(new_data, model_path, scaler_path, model_name=model_name)

        print("✅ Model updated!" if model_updated else "ℹ️ No update needed.")

    except Exception as e:
        print(f"❌ Error during background training: {str(e)}")


@app.post("/update_model_async")
def update_model_async(
    city: str,
    model_name: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials)
    thread = threading.Thread(target=run_training, args=(city, model_name))
    thread.start()

    return {"message": "Training started in the background. You can continue using the API."}

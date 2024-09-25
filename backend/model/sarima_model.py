from backend.api.geocode import get_coordinates
from backend.api.open_meteo import get_temperature, get_history
import requests
import dotenv
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from datetime import datetime, timedelta
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

dotenv.load_dotenv()


def initialize_LSTM_model(sequence_length):
    """
    Initializes and returns an LSTM model for time series forecasting.
    The model consists of two LSTM layers with 100 units each, followed by dropout layers to prevent overfitting,
    and a dense layer with a single unit for the output. The model is compiled with the Adam optimizer and
    mean squared error loss function, and it also tracks mean absolute error as a metric.
    Parameters:
    sequence_length (int): The length of the input sequences.
    Returns:
    keras.models.Sequential: The compiled LSTM model.
    """

    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

def data_daily(history):
    """
    Converts hourly weather data to daily averages.
    Parameters:
    history (dict): A dictionary containing 'time' and 'temperature_2m' keys with corresponding lists of hourly data.
    Returns:
    pd.DataFrame: A DataFrame with daily averaged temperature data, indexed by date.
    """
    df = pd.DataFrame({'date': history['time'], 'temperature': history['temperature_2m']})
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df_daily = df.resample('D').mean()
    df_daily.dropna(inplace=True)
    return df_daily

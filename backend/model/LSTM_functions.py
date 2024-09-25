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


def initialize_LSTM_model(sequence_length, forecast_horizon):
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
    model.add(Dense(forecast_horizon))
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
def scale_data(df):
    """
    Scales the temperature data in the given DataFrame using MinMaxScaler.
    Parameters:
    df (pandas.DataFrame): DataFrame containing the temperature data to be scaled.
    Returns:
    tuple: A tuple containing:
        - scaled_temps (numpy.ndarray): Scaled temperature values.
        - scaler (MinMaxScaler): The scaler object used for scaling.
    """

    temperature = df['temperature'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_temps = scaler.fit_transform(temperature)
    return scaled_temps, scaler

def create_sequences(data, sequence_length, forecast_horizon=1):
    """
    Generates sequences of data for time series forecasting.
    Parameters:
    data (array-like): The input time series data.
    sequence_length (int): The length of each input sequence.
    forecast_horizon (int, optional): The number of time steps to forecast. Defaults to 1.
    Returns:
    tuple: A tuple containing two numpy arrays:
        - x (numpy array): The input sequences of shape (num_sequences, sequence_length).
        - y (numpy array): The corresponding target sequences of shape (num_sequences, forecast_horizon).
    """

    x, y = [], []
    for i in range(len(data) - sequence_length - forecast_horizon):
        x.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length:i+sequence_length+forecast_horizon])
    return np.array(x), np.array(y)


def fit_LSTM_model(data, split_factor = 0.8, sequence_length = 168, forecast_horizon = 24):
    """
    Fits an LSTM model to the provided time series data.
    Parameters:
    data (pd.DataFrame or np.ndarray): The input time series data.
    split_factor (float, optional): The fraction of data to be used for training. Default is 0.8.
    sequence_length (int, optional): The length of the input sequences. Default is 168.
    forecast_horizon (int, optional): The number of time steps to forecast. Default is 24.
    Returns:
    tuple: A tuple containing:
        - history (keras.callbacks.History): The history object generated after training the model.
        - model (keras.Model): The trained LSTM model.
        - scaler (sklearn.preprocessing.StandardScaler): The scaler used to normalize the data.
    """

    scaled_temps, scaler = scale_data(data)
    X, y = create_sequences(scaled_temps, sequence_length,forecast_horizon)
    split = int(split_factor * len(X))  # 80% pour l'entraînement, 20% pour le test
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    model = initialize_LSTM_model(sequence_length, forecast_horizon)
    history = model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test, y_test))
    return history, model, scaler

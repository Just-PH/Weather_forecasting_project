import dotenv
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
import joblib
dotenv.load_dotenv()


def initialize_LSTM_model(sequence_length=336, forecast_horizon=48):
    """
    Initializes and returns an LSTM model for time series forecasting.
    The model consists of two LSTM layers with 100 units each, followed by dropout layers to prevent overfitting,
    and a dense layer with 'forecast_horizon' units for the output. The model is compiled with the Adam optimizer and
    mean squared error loss function, and it also tracks mean absolute error as a metric.

    Parameters:
    sequence_length (int): The length of the input sequences.
    forecast_horizon (int): The number of future time steps to forecast.

    Returns:
    keras.models.Sequential: The compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))  # `return_sequences=False` for the final LSTM layer
    model.add(Dropout(0.2))
    model.add(Dense(forecast_horizon))  # Output layer for 'forecast_horizon' predictions
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    return model


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


def create_sequences(data, sequence_length=336, forecast_horizon=48):
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


def fit_LSTM_model(data, split_factor=0.8, sequence_length=336, forecast_horizon=48, model_name=None):
    """
    Fits an LSTM model to the provided time series data.

    Parameters:
    data (pd.DataFrame or np.ndarray): The input time series data.
    split_factor (float, optional): The fraction of data to be used for training. Default is 0.8.
    sequence_length (int, optional): The length of the input sequences. Default is 336 for 2 weeks.
    forecast_horizon (int, optional): The number of time steps to forecast. Default is 48 for 2 days.

    Returns:
    tuple: A tuple containing:
        - history (keras.callbacks.History): The history object generated after training the model.
        - model (keras.Model): The trained LSTM model.
        - scaler (sklearn.preprocessing.StandardScaler): The scaler used to normalize the data.
    """
    # Scale the data
    scaled_temps, scaler = scale_data(data)

    # Create sequences for training
    X, y = create_sequences(scaled_temps, sequence_length, forecast_horizon)

    # Split into training and testing sets
    split = int(split_factor * len(X))  # 80% training, 20% testing
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Initialize the LSTM model
    model = initialize_LSTM_model(sequence_length, forecast_horizon)

    # Train the model
    history = model.fit(X_train, y_train, epochs=30, batch_size=64, validation_data=(X_test, y_test),
                        callbacks=[EarlyStopping(patience=2)], verbose=1)

    # Save the model
    if model_name:
        save_dir = os.path.join(os.path.dirname(__file__), 'model_saved')
        model.save(os.path.join(save_dir, f'{model_name}.keras'))

    # Save the scaler using joblib
    if model_name:
        save_dir = os.path.join(os.path.dirname(__file__), 'model_saved')
        joblib.dump(scaler, os.path.join(save_dir, f'{model_name}_scaler.pkl'))

    return history, model, scaler


def retrain_and_compare_LSTM(new_data, model_path, scaler_path, split_factor=0.8, sequence_length=336, forecast_horizon=48, model_name=None):
    """
    Retrains an LSTM model with new data, then compares the performance of the new model with the old one.
    If the new model performs better, it replaces the old model.

    Parameters:
    new_data (pd.DataFrame or np.ndarray): The new data for retraining the model.
    model_path (str): The path to the existing LSTM model.
    scaler_path (str): The path to the existing scaler.
    split_factor (float, optional): The fraction of data used for training. Default is 0.8.
    sequence_length (int, optional): The length of the input sequences. Default is 336 (2 weeks).
    forecast_horizon (int, optional): The number of time steps to forecast. Default is 48 (2 days).
    model_name (str, optional): The name to save the updated model if it's better.

    Returns:
    tuple: A tuple containing:
        - history (keras.callbacks.History): The training history of the model.
        - model (keras.Model): The retrained LSTM model or the old model.
        - scaler (sklearn.preprocessing.StandardScaler): The scaler used for normalizing the data.
        - model_updated (bool): Indicates whether the model was updated.
    """
    # Load the existing model and scaler
    model, scaler = load_LSTM_model(model_path, scaler_path)

    # Update the data by scaling and creating sequences
    scaled_temps, _ = scale_data(new_data)
    X, y = create_sequences(scaled_temps, sequence_length, forecast_horizon)

    # Split the data into training and test sets
    split = int(split_factor * len(X))  # 80% for training, 20% for testing
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Retrain the model with the new data
    history = model.fit(X_train, y_train, epochs=30, batch_size=64, validation_data=(X_test, y_test),
                        callbacks=[EarlyStopping(patience=2)], verbose=1)

    # Evaluate the performance of the old model and the new model
    old_model_loss, old_model_mae = model.evaluate(X_test, y_test, verbose=0)

    # Create a new model and retrain
    new_model = initialize_LSTM_model(sequence_length, forecast_horizon)
    new_history = new_model.fit(X_train, y_train, epochs=30, batch_size=64, validation_data=(X_test, y_test),
                                callbacks=[EarlyStopping(patience=2)], verbose=0)

    # Evaluate the new model
    new_model_loss, new_model_mae = new_model.evaluate(X_test, y_test, verbose=0)

    # Compare the performance (use MAE as the criterion)
    model_updated = False
    if new_model_mae < old_model_mae:  # We use MAE for comparison
        print(f"The new model is better with MAE {new_model_mae:.4f} vs {old_model_mae:.4f}.")
        model = new_model
        model_updated = True

        # Save the updated model and scaler
        if model_name:
            save_dir = os.path.join(os.path.dirname(__file__), 'model_saved')
            model.save(os.path.join(save_dir, f'{model_name}.keras'))
            joblib.dump(scaler, os.path.join(save_dir, f'{model_name}_scaler.pkl'))
    else:
        print(f"The existing model is better with MAE {old_model_mae:.4f}.")

    return history, model, scaler, model_updated


def load_LSTM_model(model_path, scaler_path):
    """
    Load a pre-trained LSTM model and its corresponding scaler from disk.

    Parameters:
    model_path (str): The file path to the saved model.
    scaler_path (str): The file path to the saved scaler.

    Returns:
    tuple: A tuple containing:
        - model (keras.Model): The loaded LSTM model.
        - scaler (sklearn.preprocessing.StandardScaler): The loaded scaler object.
    """
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def predict_from_model(df, model, scaler, sequence_length=336, forecast_horizon=48):
    """
    Predict future temperatures using a trained LSTM model.

    Parameters:
    df (pd.DataFrame): The input data containing a 'temperature' column and a datetime index.
    model (keras.Model): The trained LSTM model used for prediction.
    scaler (sklearn.preprocessing.StandardScaler): The scaler used to normalize and inverse transform the data.
    sequence_length (int, optional): The length of the input sequences for the LSTM model. Default is 336.
    forecast_horizon (int, optional): The number of future time steps to predict. Default is 48.

    Returns:
    pd.DataFrame: A DataFrame containing the predicted temperatures with corresponding dates.
    """
    data = df[-sequence_length:]
    temperature_to_pred = data['temperature'].values.reshape(-1, 1)
    scaled_temps_to_pred = scaler.transform(temperature_to_pred)
    X = scaled_temps_to_pred[-sequence_length:].reshape(1,sequence_length, 1)
    forecast_scaled = model.predict(X)
    forecast = scaler.inverse_transform(forecast_scaled)
    next_day_dates = pd.date_range(data['date'].iloc[-1] + pd.Timedelta(hours=1), periods=forecast_horizon, freq='H')
    df_forecast = pd.DataFrame({'date': next_day_dates, 'predicted_temperature': forecast[0]})

    return df_forecast

import requests
def get_temperature(lat, lng):
    """
    Fetches the current temperature for a given latitude and longitude using the Open-Meteo API.
    Args:
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.
    Returns:
        float: The current temperature in degrees Celsius if the request is successful.
        None: If the request fails or an error occurs.
    """


    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data['current_weather']['temperature'])
    else:
        print(f"Erreur {response.status_code}")
        return None

def get_history(lat,lng, start_date, end_date):
    """
    Fetch historical weather data for a specific location and date range.
    This function retrieves hourly temperature data from the Open-Meteo archive API
    for the given latitude, longitude, start date, and end date.
    Parameters:
    lat (float): Latitude of the location.
    lng (float): Longitude of the location.
    start_date (str): Start date in the format 'YYYY-MM-DD'.
    end_date (str): End date in the format 'YYYY-MM-DD'.
    Returns:
    dict: A dictionary containing hourly temperature data if the request is successful.
    None: If the request fails, returns None and prints an error message with the status code.
    """

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['hourly']
    else:
        print(f"Erreur {response.status_code}")
        return None

# if __name__:  # pragma: no cover
#     print(get_temperature(48.8566, 2.3522))  # Exemple pour Paris
#     print(get_history(48.8566, 2.3522, "2021-01-01", "2021-01-02"))  # Exemple pour Paris

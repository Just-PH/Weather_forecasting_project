# api/open_meteo.py
import requests

def get_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['current_weather']['temperature']
    else:
        return None

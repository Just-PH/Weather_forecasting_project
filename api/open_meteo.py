import requests

def get_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['current_weather']['temperature']
    else:
        print(f"Erreur {response.status_code}")
        return None

# if __name__:  # pragma: no cover
#     print(get_temperature(48.8566, 2.3522))  # Exemple pour Paris

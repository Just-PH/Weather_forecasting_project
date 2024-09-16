import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv(dotenv_path='.env')

# Récupérer la clé API depuis le fichier .env
API_KEY = os.getenv('API_KEY_GEOCODE')

def get_coordinates(city_name, API_KEY = API_KEY):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']  # Latitude et Longitude
    return None, None

# if __name__ == "__main__":
#     print(f"Api Key: {API_KEY}") # Test pour afficher la clé API
#     print(get_coordinates("Paris"))  # Exemple pour Paris

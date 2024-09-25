import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API depuis le fichier .env
API_KEY = os.getenv('API_KEY_GEOCODE')

def get_coordinates(city_name, API_KEY = API_KEY):
    def get_coordinates(city_name, API_KEY=API_KEY):
        """
        Fetches the geographical coordinates (latitude and longitude) of a given city using the OpenCage Geocoding API.
        Args:
            city_name (str): The name of the city for which to fetch coordinates.
            API_KEY (str): The API key for accessing the OpenCage Geocoding API.
        Returns:
            dict: A dictionary containing the latitude ('lat') and longitude ('lng') of the city if found.
            None: If the city is not found or an error occurs, returns None.
        """

    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            geometry = data['results'][0]['geometry']
            return {'lat': geometry['lat'],'lng' : geometry['lng']}  # Latitude et Longitude
    return None, None

# if __name__ == "__main__":
#     print(f"Api Key: {API_KEY}") # Test pour afficher la clé API
#     print(get_coordinates("Paris"))  # Exemple pour Paris

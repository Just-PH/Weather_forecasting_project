from fastapi import FastAPI
from backend.api.geocode import get_coordinates
from backend.api.open_meteo import get_temperature
app = FastAPI()

# define a root '/' endpoint
@app.get("/")
def index():
    return {"message": "Hello, World"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}"}

@app.get("/temperature/{city}")
def temperature(city: str):
    data = get_coordinates(city)
    temp = get_temperature(data['lat'], data['lng'])
    data['temperature'] = temp
    return data

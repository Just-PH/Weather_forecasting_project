# Weather_forecasting_project
Predict the weather of the day and compare it to other prediction

# Setup

You need to make a .env file containing your api key from open-meteo :
```
API_KEY_GEOCODE = ...
```
# Docker
To build the image run :
```
docker build -t image-name .
```
To run the image locally:
```
docker run --env-file .env -p 8000:8082 image-name
```

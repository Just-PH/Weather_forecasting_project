# Weather_forecasting_project
Predict the weather of the day and compare it to other prediction

# Docker
To build the image run :
```
docker build -t image-name .
```
To run the image locally:
```
docker run --env-file .env -p 8000:8082 image-name
```

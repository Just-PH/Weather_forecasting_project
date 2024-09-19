FROM python:3.10.6-slim-buster
WORKDIR /app
COPY backend /app/backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "backend.back:app", "--port", "8000", "--host", "0.0.0.0"]

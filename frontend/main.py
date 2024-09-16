# frontend/main.py
import streamlit as st
from api.main import get_temperature

# Appliquer le style CSS pour changer le fond en blanc
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("App Météo avec Open-Meteo API")

lat = st.number_input("Entrez la latitude", value=48.8566)  # Exemple pour Paris
lon = st.number_input("Entrez la longitude", value=2.3522)  # Exemple pour Paris

if st.button("Obtenir la température"):
    temperature = get_temperature(lat, lon)
    if temperature is not None:
        st.success(f"La température actuelle est de {temperature}°C")
    else:
        st.error("Impossible de récupérer la température, essayez à nouveau.")

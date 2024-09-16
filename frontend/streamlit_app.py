import streamlit as st
from api.open_meteo import get_temperature
from api.geocode import get_coordinates

def run_app():
    # Appliquer le style CSS pour changer le fond en blanc
    st.markdown("""
        <style>
        body {
            background-color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("App Météo avec Open-Meteo API")

    city_name = st.text_input("Entrez le nom de la ville", value="Paris")

    if st.button("Obtenir la température"):
        lat, lon = get_coordinates(city_name)  # Obtenir la latitude et la longitude de la ville
        if lat and lon:
            st.write(f"Coordonnées trouvées : {lat}, {lon}")
            temperature = get_temperature(lat, lon)
            if temperature:
                st.success(f"La température actuelle à {city_name} est de {temperature}°C")
            else:
                st.error("Impossible de récupérer la température.")
        else:
            st.error("Ville introuvable, veuillez essayer à nouveau.")

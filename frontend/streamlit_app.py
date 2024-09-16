import streamlit as st
from api.open_meteo import get_temperature
from api.geocode import get_coordinates
import base64
import os
from io import BytesIO

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        .title{{
            color: black;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def load_custom_css():
    st.markdown(
        """
        <style>
        .title {
            color: black;  # Couleur du texte en noir
            font-size: 36px;  # Taille du texte
        }
        .stTextInput label {
        color: black;  /* Couleur du texte du label en noir */
        font-size: 30px;  /* Taille du texte */
        }
        .stText, .stAlert p, .stMarkdown p {
        color: black;  /* Couleur du texte en noir */
        }
        .stAlert {
            background-color: #f0f0f0;  /* Couleur de fond pour les alertes (st.success, st.error) */
            color : black;  /* Couleur du texte */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def run_app():

    # Adding a background image
    add_bg_from_local(os.path.join(os.getcwd(), 'images', 'background.jpeg'))
    load_custom_css()

    # Afficher le titre avec la classe CSS
    st.markdown('<h1 class="title">Météo du Jour </h1>', unsafe_allow_html=True)
    city_name = st.text_input("Entrez le nom de la ville", value="Paris")

    if st.button("Obtenir la température"):
        lat, lon = get_coordinates(city_name)  # Obtenir la latitude et la longitude de la ville
        if lat and lon:
            st.write(f"Coordonnées trouvées : lat = {lat}, lon = {lon}")
            temperature = get_temperature(lat, lon)
            if temperature:
                st.success(f"La température actuelle à {city_name} est de {temperature}°C")
            else:
                st.error("Impossible de récupérer la température.")
        else:
            st.error("Ville introuvable, veuillez essayer à nouveau.")

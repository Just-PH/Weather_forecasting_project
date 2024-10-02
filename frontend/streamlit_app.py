import streamlit as st
import base64
import os
import requests
from datetime import datetime
import pandas as pd  # Assurez-vous d'importer pandas
import plotly.express as px
import plotly.graph_objects as go
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

def run_app(url):
    # Adding a background image
    add_bg_from_local(os.path.join(os.getcwd(), 'images', 'background.jpeg'))
    load_custom_css()

    # Afficher le titre avec la classe CSS
    st.markdown('<h1 class="title">Météo du Jour </h1>', unsafe_allow_html=True)
    city_name = st.text_input("Entrez le nom de la ville", value="Paris")

    # Gestion des résultats via session_state
    if 'temperature_result' not in st.session_state:
        st.session_state.temperature_result = None
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None

    # Ajouter les boutons sur la même ligne avec `st.columns`
    col1, col2 = st.columns([1,2])

    with col1:
        if st.button("Température actuelle"):
            response = requests.get(f"{url}/temperature/{city_name}")
            if response.status_code == 200:
                data = response.json()
                lat = data.get('lat')
                lng = data.get('lng')
                temperature = data.get('temperature')
                if lat and lng:
                    st.session_state.temperature_result = f"<span style='font-size:24px; font-weight:bold;'>\
                        La température actuelle à {city_name} est de {temperature}°C</span>"

                else:
                    st.session_state.temperature_result = "Ville introuvable, veuillez essayer à nouveau."
            else:
                st.session_state.temperature_result = "Erreur lors de la requête API."

    with col2:
        if st.button("Prévisions de température du jour"):
            response = requests.get(f"{url}/predict_temperature/{city_name}")
            if response.status_code == 200:
                data = response.json()
                prediction = {datetime.strptime(k, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M'): v for k, v in data.items()}
                st.session_state.prediction_result = prediction
            else:
                st.session_state.prediction_result = "Erreur lors de la requête API pour la prédiction."

    # Afficher les résultats sous les boutons
    with col1:
        if st.session_state.temperature_result:
            st.markdown(st.session_state.temperature_result, unsafe_allow_html=True)

    with col2:
        if isinstance(st.session_state.prediction_result, dict):
            # Convertir le dictionnaire en DataFrame
            df = pd.DataFrame(list(st.session_state.prediction_result.items()), columns=['Heure', 'Température']).set_index('Heure')
            x_values = df.index
            y_values = df['Température']
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers',
                marker=dict(size=10, color='lightblue'),
                line_shape='spline',
                hovertemplate='<span style="font-size: 18px;">%{x} : T = %{y}°C</span>',
                name=""
            ))
            fig.update_layout(
                title=f"Prédiction des températures pour {city_name}",
                xaxis_title="Heure",
                yaxis_title="Température (°C)",
                xaxis_tickangle=-45,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

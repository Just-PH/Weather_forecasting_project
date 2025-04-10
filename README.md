# 🌤️ Weather Forecasting Project

## 🎯 Objectif
Ce projet a pour but de prédire les températures futures d'une ville donnée en combinant des données météo en temps réel avec des modèles de machine learning, le tout encapsulé dans une architecture client-serveur industrialisable.

## 🧱 Stack technique
- **Backend** : Python, FastAPI  
- **Modélisation** : LSTM (Keras), modèles classiques (XGBoost, Random Forest)  
- **Frontend** : Streamlit (version initiale), puis application React avec appel à l’API  
- **Infrastructure** : Docker, Google Cloud Platform (déploiement avec Cloud Run), Makefile, gestion des variables avec `.env`

## ⚙️ Fonctionnalités clés
- 📡 **Récupération des données météo** via l’API Open-Meteo
- 🧼 **Nettoyage et structuration** des séries temporelles horaires
- 🧠 **Entraînement de modèles** de prédiction de température (LSTM et modèles de comparaison)
- 🔌 **Création d’API** avec FastAPI pour exposer les prédictions de température
- 💻 **Interface utilisateur** simple (Streamlit) ou moderne (React)
- 📦 **Déploiement Dockerisé** prêt pour le cloud (GCP)

## 🔍 Pourquoi ce projet ?
Ce projet met en pratique :
- L'intégration complète d’un **modèle de machine learning dans une API** consommable
- La manipulation de **séries temporelles réelles** et bruitées
- La conception d’un **système modulaire, scalable et déployable**
- Une bonne séparation des responsabilités entre **front**, **back**, et **modèle ML**

## 📌 À venir (ou idées d’amélioration)
- Prise en compte de plusieurs types de variables météo (précipitations, humidité…)
- Sélection automatique du meilleur modèle selon la localisation
- Ajout d’un système de logs et d’erreurs plus robuste
- Monitoring avec Prometheus + Grafana
"""


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

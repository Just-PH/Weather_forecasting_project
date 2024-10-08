import React, { useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';

// Enregistre les composants nécessaires
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [cityName, setCityName] = useState('Paris');
  const [temperature, setTemperature] = useState(null);
  const [forecast, setForecast] = useState(null);
  const API_URL = process.env.REACT_APP_BACK_API;

  const handleTemperatureFetch = async () => {
    try {
      const response = await axios.get(`${API_URL}/temperature/${cityName}`);
      if (response.status === 200) {
        const data = response.data;
        setTemperature(data.temperature);
      } else {
        setTemperature(`Erreur lors de la requête API.`);
      }
    } catch (error) {
      setTemperature(`Erreur lors de la requête API. (erreur : ${error.message})`);
    }
  };

  const handleForecastFetch = async () => {
    try {
      const response = await axios.get(`${API_URL}/predict_temperature/${cityName}`);
      if (response.status === 200) {
        const data = response.data;
        const forecastData = {
          labels: Object.keys(data),
          datasets: [
            {
              label: 'Température (°C)',
              data: Object.values(data),
              borderColor: 'rgba(75,192,192,1)',
              backgroundColor: 'rgba(75,192,192,0.2)',
              pointBorderColor: 'rgba(75,192,192,1)',
              pointBackgroundColor: '#fff',
              pointHoverRadius: 5,
              pointHoverBackgroundColor: 'rgba(75,192,192,1)',
              pointRadius: 1,
              pointHitRadius: 10,
            },
          ],
        };
        setForecast(forecastData);
      } else {
        setForecast(`Erreur lors de la requête API pour la prédiction.`);
      }
    } catch (error) {
      setForecast(`Erreur lors de la requête API. (erreur : ${error.message})`);
    }
  };

  return (
    <div className="App">
      <h1>Météo du Jour</h1>
      <input
        type="text"
        value={cityName}
        onChange={(e) => setCityName(e.target.value)}
        placeholder="Entrez le nom de la ville"
      />
      <button onClick={handleTemperatureFetch}>Température actuelle</button>
      <button onClick={handleForecastFetch}>Prévisions de température du jour</button>
      {temperature && (
        <div>
          <h2>La température actuelle à {cityName} est de {temperature}°C</h2>
        </div>
      )}
      {forecast && typeof forecast === 'object' && (
        <div>
          <h2>Prédictions de température pour la journée</h2>
          <Line data={forecast} />
        </div>
      )}
    </div>
  );
}

export default App;

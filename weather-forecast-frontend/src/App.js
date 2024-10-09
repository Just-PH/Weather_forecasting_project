import React, { useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';
import { format } from 'date-fns';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [cityName, setCityName] = useState('Paris');
  const [temperature, setTemperature] = useState(null);
  const [forecast, setForecast] = useState(null);
  const API_URL = process.env.REACT_APP_BACK_API;

  const handleTemperatureFetch = async () => {
    console.log('Début de la requête température');
    const startTime = Date.now();
    try {
      const response = await axios.get(`${API_URL}/temperature/${cityName}`);
      if (response.status === 200) {
        console.log('Réponse reçue après', Date.now() - startTime, 'ms');
        setTemperature(response.data.temperature);
      } else {
        setTemperature('Erreur lors de la requête API.');
      }
    } catch (error) {
      setTemperature(`Erreur lors de la requête API. (erreur : ${error.message})`);
    }
  };

  const handleForecastFetch = async () => {
    try {
      console.log('Début de la requête prédiction');
      const startTime = Date.now();
      const response = await axios.get(`${API_URL}/predict_temperature/${cityName}`);
      if (response.status === 200) {
        console.log('Réponse reçue après', Date.now() - startTime, 'ms');
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
            },
          ],
        };
        setForecast(forecastData);
      } else {
        setForecast('Erreur lors de la requête API pour la prédiction.');
      }
    } catch (error) {
      setForecast(`Erreur lors de la requête API. (erreur : ${error.message})`);
    }
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
          tooltipFormat: 'HH:mm',
          displayFormats: { hour: 'HH:mm' },
        },
        ticks: {
          callback: function(value) {
            return format(new Date(value), 'HH:mm');
          },
        },
      },
    },
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
      <div className="column-container">
        <div className="column">
          <button onClick={handleTemperatureFetch}>Température actuelle</button>
          {temperature && (
            <div className="result">
              <h2>La température actuelle à {cityName} est de {temperature}°C</h2>
            </div>
          )}
        </div>
        <div className="column">
          <button onClick={handleForecastFetch}>Prévisions de température du jour</button>
          {forecast && typeof forecast === 'object' && (
            <div className="result chart-container">
              <h2>Prédictions de températures pour la journée</h2>
              <Line data={forecast} options={options} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


export default App;

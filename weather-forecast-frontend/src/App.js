import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [cityName, setCityName] = useState('Paris');
  const [temperature, setTemperature] = useState(null);
  const API_URL = process.env.REACT_APP_BACK_API; // Assure-toi que cela est bien défini dans .env

  const handleTemperatureFetch = async () => {
    try {
      // Requête API directe à l'URL complète
      const response = await axios.get(`${API_URL}/temperature/${cityName}`);
      if (response.status === 200) {
        const data = response.data;
        setTemperature(data.temperature); // Assure-toi que la structure de la réponse est correcte
      } else {
        setTemperature(`Erreur lors de la requête API.`);
      }
    } catch (error) {
      setTemperature(`Erreur lors de la requête API. (erreur : ${error.message})`);
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
      {temperature && (
        <div>
          <h2>La température actuelle à {cityName} est de {temperature}°C</h2>
        </div>
      )}
    </div>
  );
}

export default App;

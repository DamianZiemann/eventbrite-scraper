const axios = require('axios');

const apiKey = '59a116712fc94d10b941b16debd25d20'; // Ersetze mit deinem echten API Key
const q = 'Start-Up'; // Suchbegriff
const sortBy = 'popularity';
const userAgent = 'StartupEventFinder';

function getNews() {
  const today = new Date();
  const startDate = new Date(today);
  startDate.setDate(today.getDate() - 18); // 18 Tage zurück

  const startDateString = startDate.toISOString().split('T')[0]; // Format: YYYY-MM-DD
  const url = `https://newsapi.org/v2/everything?q=${q}&from=${startDateString}&sortBy=${sortBy}&apiKey=${apiKey}`;

  const config = {
    headers: {
      'User-Agent': userAgent
    }
  };

  axios.get(url, config)
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error('Fehler beim Abrufen der News:', error);
    });
}

getNews();



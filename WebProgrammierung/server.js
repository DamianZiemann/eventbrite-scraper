const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

const newsApiKey = '59a116712fc94d10b941b16debd25d20'; // NewsAPI Key
const huggingFaceApiKey = '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'; // Hugging Face API Key
const sortBy = 'relevancy';
const userAgent = 'StartupEventFinder';

async function summarizeText(text) {
  try {
    const response = await axios.post(
      'https://api-inference.huggingface.co/models/facebook/bart-large-cnn',
      { inputs: `Fasse die folgenden Nachrichten in einer verständlichen, kurzen Zusammenfassung zusammen: ${text}` },
      {
        headers: {
          Authorization: `Bearer ${huggingFaceApiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data[0]?.summary_text || 'Keine Zusammenfassung verfügbar.';
  } catch (error) {
    console.error('Fehler bei der Zusammenfassung:', error.message);
    return 'Zusammenfassung nicht verfügbar.';
  }
}

app.get('/news', async (req, res) => {
  try {
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(today.getDate() - 18);

    const startDateString = startDate.toISOString().split('T')[0];
    const url = `https://newsapi.org/v2/everything?q=Start-Up&from=${startDateString}&sortBy=${sortBy}&language=de&apiKey=${newsApiKey}`;

    const config = {
      headers: {
        'User-Agent': userAgent,
      },
    };

    const response = await axios.get(url, config);
    const articles = response.data.articles;

    if (!articles.length) {
      return res.json({ summary: 'Keine Nachrichten gefunden.', articles: [] });
    }

    // 1️⃣ Erste 5 Artikel holen und Texte kombinieren
    const topArticles = articles.slice(0, 3);
    const combinedText = topArticles.map(a => 
      `Titel: ${a.title}. Beschreibung: ${a.description || 'Keine Beschreibung verfügbar.'}`
    ).join(' ');

    // 2️⃣ Nachrichten zusammenfassen
    const summary = await summarizeText(combinedText);

    // 3️⃣ Rückgabe: Zusammenfassung + alle Artikel
    res.json({ summary, articles });
  } catch (error) {
    console.error('Fehler beim Abrufen der News:', error.message);
    res.status(500).json({ error: 'Fehler beim Abrufen der News' });
  }
});

app.listen(port, () => {
  console.log(`Server läuft auf Port ${port}`);
});






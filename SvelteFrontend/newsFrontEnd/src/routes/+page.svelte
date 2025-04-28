<script>
  import { onMount, onDestroy } from 'svelte';
  import Header from './Header/Header.svelte';

  let articles = [];
  let filter = 'popularity';
  let menuOpen = false;
  let summary = ''; // Zusammenfassung für die Top 5 Artikel

  function closeMenu(event) {
    if (!event.target.closest("nav") && !event.target.closest(".menu-icon")) {
      menuOpen = false;
    }
  }

  onMount(() => {
    if (typeof document !== "undefined") {
      document.addEventListener("click", closeMenu);
    }
    getNews();
  });

  onDestroy(() => {
    if (typeof document !== "undefined") {
      document.removeEventListener("click", closeMenu);
    }
  });

  async function getNews() {
    try {
      const response = await fetch('http://localhost:3000/news');
      if (!response.ok) throw new Error(`HTTP-Fehler: ${response.status}`);
      const data = await response.json();

      summary = data.summary || ''; // Speichert die Zusammenfassung

      articles = data.articles || [];
    } catch (error) {
      console.error('Fehler beim Abrufen der News:', error);
    }
  }

  function sortArticles(articles, filter) {
    if (!Array.isArray(articles)) return [];

    return [...articles].sort((a, b) => {
      switch (filter) {
        case 'newest':
          return new Date(b.publishedAt || 0) - new Date(a.publishedAt || 0);
        case 'oldest':
          return new Date(a.publishedAt || 0) - new Date(b.publishedAt || 0);
        case 'abc':
          return (a.title || '').localeCompare(b.title || '');
        default:
          return 0; 
      }
    });
  }

  $: sortedArticles = sortArticles(articles, filter);
</script>

<header class="header">
  <button class="menu-icon" aria-label="Open Menu" on:click={() => menuOpen = !menuOpen}>
    ☰
  </button>
  <div class="logo">Pitchload</div>
  <nav class:open={menuOpen}>
    <ul>
      <li><a href="/">News</a></li>
      <li><a href="/map">Map</a></li>
      <li><a href="/Liste">List</a></li>
    </ul>
  </nav>
</header>

<div class="filter-buttons">
  <button on:click={() => filter = 'popularity'} class:active={filter === 'popularity'}>Popularity</button>
  <button on:click={() => filter = 'newest'} class:active={filter === 'newest'}>Newest</button>
  <button on:click={() => filter = 'oldest'} class:active={filter === 'oldest'}>Oldest</button>
  <button on:click={() => filter = 'abc'} class:active={filter === 'abc'}>Alphabetically</button>
</div>

{#if summary}
  <div class="summary-box">
    <h2>News Summary</h2>
    <p>{summary}</p>
  </div>
{/if}

<ul class="news-list">
  {#each sortedArticles as article}
    {#if article.url && !article.url.includes('consent.yahoo.com')}
      <li class="news-item">
        <div class="news-image-container">
          {#if article.urlToImage}
            <img src={article.urlToImage} alt={article.title} class="news-image" />
          {/if}
        </div>
        <div class="news-content">
          <h3><a href={article.url} target="_blank">{article.title}</a></h3>
          <p>{article.description}</p>
          <span class="source">{article.source?.name} - {new Date(article.publishedAt).toLocaleDateString()}</span>
        </div>
      </li>
    {/if}
  {/each}
</ul>

<style>
  :root {
    --primary-color: #f5f5f5;
    --secondary-color: #8367b4;
    --text-color: #333;
    --header-background: #fff;
  }

  * {
    font-family: 'Arial', sans-serif !important;
  }

  body {
    background-color: var(--primary-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
  }

  .header {
    font-style: italic;
    background-color: var(--header-background);
    padding: 20px;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
  }

  .menu-icon {
    font-size: 1.8em;
    cursor: pointer;
    margin-right: 20px;
    padding: 10px;
    user-select: none;
    background: none;
    border: none;
    color: var(--text-color);
  }

  .header .logo {
    font-size: 1.5em;
    font-weight: bold;
  }

  .header nav {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: var(--header-background);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: none;
  }

  .header nav.open {
    display: block;
  }

  .header nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .header nav ul li {
    margin: 10px 0;
  }

  .header nav ul li a {
    text-decoration: none;
    color: var(--text-color);
  }

  .news-list {
    list-style: none;
    padding: 0;
  }

  .news-item {
    display: flex;
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
  }

  .news-image-container {
    width: 200px;
    margin-right: 20px;
  }

  .news-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .news-content {
    flex: 1;
  }

  .news-content h3 {
    margin-bottom: 5px;
  }

  .news-content a {
    text-decoration: none;
    color: var(--text-color);
  }

  .news-content p {
    margin-bottom: 5px;
  }

  .source {
    font-size: 0.8em;
    color: #888;
  }

  .filter-buttons {
    display: flex;
    justify-content: center;
    margin: 30px 0 20px;
  }

  .filter-buttons button {
    all: unset;
    display: inline-block;
    padding: 12px 20px;
    margin: 0 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
    color: var(--text-color);
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-size: 1em;
    text-align: center;
  }

  .filter-buttons button.active {
    background-color: var(--secondary-color);
    color: #fff;
    border-color: var(--secondary-color);
  }

  .summary-box {
    background: rgb(246, 237, 255);
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 20px;
  }

  .summary-box h2 {
    font-size: 1.2em;
    margin-bottom: 10px;
  }

  .summary-box p {
    font-size: 1em;
    color: #555;
  }
</style>

// Fetch startup news
async function fetchStartupNews() {
  try {
    const response = await fetch("http://127.0.0.1:5000/news/startup");
    const data = await response.json();

    const newsContainer = document.getElementById("news-articles");
    newsContainer.innerHTML = ""; // Clear existing content

    if (data.articles && data.articles.length > 0) {
      data.articles.forEach((article) => {
        const articleElement = document.createElement("div");
        articleElement.classList.add("news-article");
        articleElement.innerHTML = `
          <h3>${article.title}</h3>
          <p>${article.description || "No description available."}</p>
          <p><strong>Source:</strong> ${article.source}</p>
          <a href="${article.url}" target="_blank">Read more</a>
        `;
        newsContainer.appendChild(articleElement);
      });
    } else {
      newsContainer.textContent = "No startup news found.";
    }
  } catch (error) {
    console.error("Error fetching startup news:", error);
    document.getElementById("news-articles").textContent =
      "Failed to load news. Please try again later.";
  }
}

// Load news on page load
document.addEventListener("DOMContentLoaded", fetchStartupNews);
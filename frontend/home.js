// Fetch upcoming events
async function fetchUpcomingEvents() {
  try {
    const response = await fetch("http://127.0.0.1:5000/events/upcoming");
    const events = await response.json();
    const eventList = document.getElementById("event-list");

    if (events.length === 0) {
      eventList.innerHTML = "<li>No upcoming events found.</li>";
      return;
    }

    events.forEach(event => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${event.title}</strong> - ${event.date} (${event.start} - ${event.end})<br>
        <a href="${event.ticket_url}" target="_blank">More Info</a>
      `;
      eventList.appendChild(li);
    });
  } catch (error) {
    console.error("Error fetching events:", error);
  }
}

// Fetch news summary
async function fetchNewsSummary() {
  try {
    const response = await fetch("http://127.0.0.1:5000/news/summary");
    const data = await response.json();
    const newsSummary = document.getElementById("news-summary");
    newsSummary.textContent = data.summary || "No news available.";
  } catch (error) {
    console.error("Error fetching news summary:", error);
  }
}

// Fetch startup news for the last week
async function fetchStartupNews() {
  try {
    const response = await fetch("http://127.0.0.1:5000/news/startup");
    const data = await response.json();
    const newsSummary = document.getElementById("news-summary");
    newsSummary.innerHTML = ""; // Clear existing content

    if (data.articles && data.articles.length > 0) {
      data.articles.forEach((article) => {
        const articleElement = document.createElement("div");
        articleElement.style.marginBottom = "1rem";
        articleElement.innerHTML = `
          <h3>${article.title}</h3>
          <p>${article.description || "No description available."}</p>
          <a href="${article.url}" target="_blank">Read more</a>
        `;
        newsSummary.appendChild(articleElement);
      });
    } else {
      newsSummary.textContent = "No startup news found.";
    }
  } catch (error) {
    console.error("Error fetching startup news:", error);
    document.getElementById("news-summary").textContent =
      "Failed to load news. Please try again later.";
  }
}

// Load data on page load
document.addEventListener("DOMContentLoaded", () => {
  fetchUpcomingEvents();
  fetchStartupNews();
});
const API_BASE_URL = "http://127.0.0.1:5000"; // Replace with your backend URL

// Fetch all organizers and populate the table
async function fetchOrganizers() {
  try {
    const response = await fetch(`${API_BASE_URL}/organizers`);
    const organizers = await response.json();
    const organizerList = document.getElementById("organizer-list");

    organizerList.innerHTML = ""; // Clear the table

    organizers.forEach((organizer) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${organizer.name}</td>
        <td><a href="${organizer.url}" target="_blank">${organizer.url}</a></td>
        <td>${organizer.id}</td>
        <td class="event-count">${organizer.event_count}</td>
      `;
      organizerList.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching organizers:", error);
  }
}

// Add a new organizer
document.getElementById("add-organizer-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const name = document.getElementById("organizer-name").value;
  const url = document.getElementById("eventbrite-link").value;
  const organizerId = document.getElementById("organizer-id").value;

  try {
    const response = await fetch(`${API_BASE_URL}/organizers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, url, pitchload_id: organizerId }),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(error.error || "Failed to add organizer");
      return;
    }

    alert("Organizer added successfully!");
    document.getElementById("add-organizer-form").reset();
    fetchOrganizers(); // Refresh the organizer list
  } catch (error) {
    console.error("Error adding organizer:", error);
  }
});

// Load organizers on page load
document.addEventListener("DOMContentLoaded", fetchOrganizers);
<script>
	import { onMount } from 'svelte';
	import Header from '../Header/Header.svelte';

	let events = [];

	async function loadAllEventData() {
		let title_all = [];
		let date_all = [];
		let start_all = [];
		let end_all = [];
		let city_all = [];
		let description_all = [];
		try {
			const response = await fetch('http://127.0.0.1:5000/events/map');

			if (!response.ok) {
				throw new Error('API responded with an error');
			}
			const data = await response.json();
			console.log("response data: "+data);
			title_all = data.map((item) => item.title);
			date_all = data.map((item) => item.date);
			start_all = data.map((item) => item.start);
			end_all = data.map((item) => item.end);
			city_all = data.map((item) => item.address_city);
			description_all = data.map((item) => item.description);
			return [title_all, date_all, start_all, end_all, city_all, description_all];
		} catch (err) {
			console.error('Error fetching data:', err);
		}
	}

	async function LoadEvents() {
		const event_all = await loadAllEventData();
		if (!Array.isArray(event_all)) {
			console.error('Title_all is not an array:', event_all);
			return;
		}
		if (event_all.length === 0) {
			console.error('No titles found');
		} else {
			console.log('Titles loaded successfully:', event_all);
		}
		// Platzhalterdaten

		const title_all = event_all[0];
		const date_all = event_all[1];
		const start_all = event_all[2];
		const end_all = event_all[3];
		const city_all = event_all[4];
		const description_all = event_all[5];

		if (title_all.length === date_all.length && title_all.length === start_all.length && title_all.length === end_all.length && title_all.length === city_all.length && title_all.length === description_all.length) {
			console.log('All arrays have the same length:', title_all.length);
		} else {
				const maxLength = Math.max(title_all.length, date_all.length, start_all.length, end_all.length, city_all.length, description_all.length);

				while (title_all.length < maxLength) {
					title_all.push('Untitled Event');
				}
				while (date_all.length < maxLength) {
					date_all.push('01 Jan 1970');
				}
				while (start_all.length < maxLength) {
					start_all.push('00:00');
				}
				while (end_all.length < maxLength) {
					end_all.push('00:00');
				}
				while (city_all.length < maxLength) {
					city_all.push('Unknown City');
				}
				while (description_all.length < maxLength) {
					description_all.push('No description available.');
				}
		}	
		events = []; 
		const images = [
			"/event_image.jpg",
			"/event_image2.jpg",
			"/event_image3.jpg",
			"/event_image4.jpg",
			"/event_image5.jpg",
		]
		for (let i = 0; i < title_all.length; i++) {
			console.log("loading event: "+title_all[i]);
			events.push({
				title: title_all[i],
				date: date_all[i],
				time: `${start_all[i]} – ${end_all[i]}`,
				location: city_all[i],
				description: description_all[i],
				isFree: true,
				image: images[i % images.length] // Rotating through the images
			});
		}

		console.log(events);
	}

	onMount(() => {
		LoadEvents();
	});
</script>

<Header />

<main class="page-wrapper">
	<div class="event-grid">
		{#each events as event}
			<div class="event-card {event.image ? 'with-img' : ''}">
			
				{#if event.image}
					<img src={event.image} alt="Event image" />
				{/if}
				<div class="event-content">
					<div class="event-header-text">
						<h3>{event.title}</h3>
						{#if event.isFree}
							<span class="badge">Free Event!</span>
						{/if}
					</div>
					<p>📅 {event.date}</p>
					<p>⏰ {event.time}</p>
					<p>📍 <strong>{event.location}</strong></p>
					<p class="desc">{event.description}</p>
				</div>
			</div>
		{/each}
	</div>
</main>

<style>
	.page-wrapper {
		padding: 1rem;
		background-color: #f5f7f5;
		font-family: Arial, sans-serif;
	}

	.event-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 0;
	}

	.filter-button {
		background: none;
		border: 1px solid #ccc;
		border-radius: 6px;
		padding: 0.4rem 0.8rem;
		cursor: pointer;
	}

	.view-toggle {
		display: flex;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.view-toggle button {
		border: 1px solid #ccc;
		background-color: #fff;
		padding: 0.5rem 1rem;
		border-radius: 20px;
		cursor: pointer;
	}

	.view-toggle .active {
		background-color: #eee;
		font-weight: bold;
	}

	.event-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 1.5rem;
	}

	.event-card {
		background-color: white;
		border-radius: 10px;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		padding: 1rem;
		display: flex;
		flex-direction: column;
	}

	.event-card.with-img img {
		border-top-left-radius: 10px;
		border-top-right-radius: 10px;
		width: 100%;
		height: 160px;
		object-fit: cover;
	}

	.event-content {
		padding: 0.5rem;
	}

	.event-header-text {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.badge {
		background-color: #7f5b9e;
		color: white;
		font-size: 0.75rem;
		padding: 0.2rem 0.5rem;
		border-radius: 5px;
	}

	.desc {
		margin-top: 0.5rem;
		color: #555;
		font-size: 0.9rem;
	}
</style>

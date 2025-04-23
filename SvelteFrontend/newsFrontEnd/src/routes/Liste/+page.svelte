<script>
	import Header from '../Header/Header.svelte';

	// Platzhalterdaten
	let events = [
		{
			title: 'Event Title 1',
			date: '01 Jan 2025',
			time: '10:00 AM – 02:00 PM',
			location: 'City 1',
			description: 'Short description of the event goes here.',
			isFree: true,
			image: null
		},
		{
			title: 'Event Title 2',
			date: '05 Jan 2025',
			time: '03:00 PM – 05:00 PM',
			location: 'City 2',
			description: 'Another event with more cool details.',
			isFree: false,
			image: '/placeholder.jpg'
		},
		{
			title: 'Event Title 3',
			date: '05 Jan 2025',
			time: '03:00 PM – 05:00 PM',
			location: 'City 2',
			description: 'Another event with more cool details.',
			isFree: true,
			image: '/placeholder.jpg'
		},
		{
			title: 'Event Title 4',
			date: '05 Jan 2025',
			time: '03:00 PM – 05:00 PM',
			location: 'City 2',
			description: 'Another event with more cool details.',
			isFree: false,
			image: '/placeholder.jpg'
		},
		{
			title: 'Event Title 5',
			date: '05 Jan 2025',
			time: '03:00 PM – 05:00 PM',
			location: 'City 2',
			description: 'Another event with more cool details.',
			isFree: true,
			image: '/placeholder.jpg'
		},
		{
			title: 'Event Title 6',
			date: '05 Jan 2025',
			time: '03:00 PM – 05:00 PM',
			location: 'City 2',
			description: 'Another event with more cool details.',
			isFree: true,
			image: '/placeholder.jpg'
		}
	];
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

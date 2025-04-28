<script>
	import maplibregl from 'maplibre-gl';
	import { onMount } from 'svelte';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import Header from '../Header/Header.svelte';

	let map;

    async function loadMap(){
        const response = await fetch("http://localhost:5000/events/map")

        if(!response.ok){
            throw new Error("API responded with an error")
        }
        const data= await response.json()
        console.log("response ",data)
        let title_all=data.map((item)=>item.title)
        let longitude_all=data.map((item)=>item.longitude)
        let latitude_all=data.map((item)=>item.latitude)
        return [title_all,longitude_all,latitude_all]
    }

	onMount(() => {
		const mapContainer = document.getElementById('map');
		if (!mapContainer) {
			console.error("Couldn't find web container");
			return;
		}

		map = new maplibregl.Map({
			container: mapContainer,
			style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json',
			center: [9.171597, 48.773439], // Zentrum (z. B. Stuttgart)
			zoom: 7
		});

		map.on('load', () => {
			console.log('Map is loading');

			// 🔹 Hier definierst du die Pins
			loadMap().then(([titles, longitudes, latitudes]) =>
                titles.map((title, index)=>{
                    const coords=[longitudes[index],latitudes[index]]

                    const popup = new maplibregl.Popup({
                        closeButton: false,
                        closeOnClick: false
				    }).setText(title);

				const marker = new maplibregl.Marker({ color: 'purple' }).setLngLat(coords).addTo(map);

				marker.getElement().addEventListener('mouseenter', () => {
					popup.setLngLat(coords).addTo(map);
				});

				marker.getElement().addEventListener('mouseleave', () => {
					popup.remove();
				});
            })
		)

			// 🔄 Für jeden Eintrag einen Marker und ein Popup erstellen
			

			console.log('Pins set');
		});
	});
</script>

<!-- Header -->
<Header />

<!-- Map Container -->
<div id="map"></div>

<style>
	:root {
		--primary-color: #f5f5f5;
		--text-color: #333;
		--header-background: #fff;
	}

	body {
		background-color: var(--primary-color);
		color: var(--text-color);
		margin: 0;
		padding: 0;
		font-family: 'Arial', sans-serif;
	}

	#map {
		width: 100%;
		height: 80vh; /* Karte nimmt 80% der Bildschirmhöhe */
	}
</style>

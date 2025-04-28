<script>
    import maplibregl from 'maplibre-gl';
    import { onMount } from 'svelte';
    import 'maplibre-gl/dist/maplibre-gl.css';
    import Header from '../Header/Header.svelte';

    let map;

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
        console.log("Map is loading");

        // 🔹 Hier definierst du die Pins
        const locations = [
    { coords: [9.217035, 49.147062], text: "📌 Writing AI Prompts for Startup Success\n           📅 24.05.2025" },
    { coords: [9.201185, 48.807974], text: "Migration Puzzle\n📅 Datum einfügen" },
    { coords: [8.365753, 49.001685], text: "KIT Innovators Homecoming\n📅 Datum einfügen" },
    { coords: [9.687133, 48.714130], text: "Start-up Talk - AI meets GP\n📅 Datum einfügen" }
    // ... weitere Events
];


        // 🔄 Für jeden Eintrag einen Marker und ein Popup erstellen
        locations.forEach(({ coords, text }) => {
            const popup = new maplibregl.Popup({
                closeButton: false,
                closeOnClick: false
            }).setText(text);

            const marker = new maplibregl.Marker({ color: 'purple' })
                .setLngLat(coords)
                .addTo(map);

            marker.getElement().addEventListener('mouseenter', () => {
                popup.setLngLat(coords).addTo(map);
            });

            marker.getElement().addEventListener('mouseleave', () => {
                popup.remove();
            });
        });

        console.log("Pins set");
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

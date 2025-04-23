<script>
    import maplibregl from 'maplibre-gl';
    import { onMount } from 'svelte';
    import 'maplibre-gl/dist/maplibre-gl.css';
    import Header from '../Header/Header.svelte';

    let map;

    onMount(() => {
        const mapContainer = document.getElementById('map');
        if (!mapContainer) {
            console.error("❌ Map-Container nicht gefunden!");
            return;
        }

        map = new maplibregl.Map({
            container: mapContainer,
            style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json',
            center: [9.171597, 48.773439], // Stuttgart, Rotebühlplatz
            zoom: 14
        });

        map.on('load', () => {
            console.log("🔄 Map geladen, füge Marker hinzu...");

            const popup = new maplibregl.Popup({
                closeButton: false,
                closeOnClick: false
            }).setText("DHBW STUTTGART");

            const marker = new maplibregl.Marker({ color: 'purple' })
                .setLngLat([9.171597, 48.773439])
                .addTo(map);

            marker.getElement().addEventListener('mouseenter', () => {
                popup.setLngLat([9.171597, 48.773439]).addTo(map);
            });

            marker.getElement().addEventListener('mouseleave', () => {
                popup.remove();
            });

            console.log("✅ Marker wurde gesetzt!", marker);
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

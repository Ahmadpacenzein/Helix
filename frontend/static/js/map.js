/* map.js - MapLibre GL map component management */

const HelixMap = {
    map: null,
    markers: [],

    /**
     * Initializes the MapLibre GL map.
     */
    init(containerId) {
        return new Promise((resolve) => {
            try {
                this.map = new maplibregl.Map({
                    container: containerId,
                    style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
                    center: [0, 20], // Centered globally
                    zoom: 1.5
                });

                this.map.addControl(new maplibregl.NavigationControl(), 'top-left');

                this.map.on('load', () => {
                    const loader = document.getElementById('map-loading');
                    if (loader) loader.classList.add('d-none');
                    resolve();
                });
            } catch (err) {
                console.error("Maplibre initialization failed:", err);
                resolve();
            }
        });
    },

    /**
     * Clears all markers from the map.
     */
    clearMarkers() {
        this.markers.forEach(marker => marker.remove());
        this.markers = [];
    },

    /**
     * Renders markers for the provided list of events.
     */
    renderEvents(events, onMarkerSelected) {
        this.clearMarkers();

        // Limit to top 1000 events to prevent browser performance degradation
        const displayEvents = events.slice(0, 1000);

        displayEvents.forEach(event => {
            const geom = event.latest_geometry;
            if (!geom || !geom.longitude || !geom.latitude) return;

            // Create custom HTML element for marker styling
            const el = document.createElement('div');
            el.className = 'helix-marker';
            
            // Adjust marker color dynamically by category
            const catId = (event.category.id || '').toLowerCase();
            if (catId.includes('wild') || catId.includes('fire')) {
                el.style.background = 'radial-gradient(circle, #f97316 0%, #c2410c 100%)';
                el.style.boxShadow = '0 0 10px rgba(249, 115, 22, 0.6)';
            } else if (catId.includes('volcano')) {
                el.style.background = 'radial-gradient(circle, #ef4444 0%, #b91c1c 100%)';
                el.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.6)';
            } else if (catId.includes('storm') || catId.includes('severe')) {
                el.style.background = 'radial-gradient(circle, #3b82f6 0%, #1d4ed8 100%)';
                el.style.boxShadow = '0 0 10px rgba(59, 130, 246, 0.6)';
            } else {
                el.style.background = 'radial-gradient(circle, #10b981 0%, #047857 100%)';
                el.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.6)';
            }

            // Create popup
            const popup = new maplibregl.Popup({ offset: 25 }).setHTML(`
                <div class="small">
                    <strong class="text-white d-block mb-1">${event.title}</strong>
                    <span class="text-secondary small d-block">Category: ${event.category.name}</span>
                    <span class="text-secondary small d-block">Status: <span class="badge ${event.status === 'open' ? 'bg-success' : 'bg-secondary'}">${event.status}</span></span>
                </div>
            `);

            // Create marker and add to map
            const marker = new maplibregl.Marker(el)
                .setLngLat([geom.longitude, geom.latitude])
                .setPopup(popup)
                .addTo(this.map);

            // Trigger detail panel display on click
            el.addEventListener('click', () => {
                if (onMarkerSelected) {
                    onMarkerSelected(event.event_id);
                }
            });

            this.markers.push(marker);
        });
    },

    /**
     * Fly the map camera smoothly to the specified coordinates.
     */
    flyTo(longitude, latitude, zoom = 6) {
        if (!this.map) return;
        this.map.flyTo({
            center: [longitude, latitude],
            zoom: zoom,
            essential: true,
            speed: 1.2
        });
    }
};

window.HelixMap = HelixMap;

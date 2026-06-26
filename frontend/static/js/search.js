/* search.js - Global search box management with debouncing */

const HelixSearch = {
    debounceTimeout: null,

    /**
     * Initializes the search input listener with debouncing.
     * @param {Function} onSearchCompleted - Callback when search returns events data.
     */
    init(onSearchCompleted) {
        const searchInput = document.getElementById('global-search');
        if (!searchInput) return;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimeout);
            const query = e.target.value.trim();

            this.debounceTimeout = setTimeout(async () => {
                try {
                    let results;
                    if (query.length > 0) {
                        results = await HelixAPI.searchEvents(query);
                    } else {
                        // If query is empty, reset to all events
                        results = await HelixAPI.getEvents();
                    }
                    
                    if (onSearchCompleted) {
                        onSearchCompleted(results, query);
                    }
                } catch (error) {
                    console.error('Search failed:', error);
                    // Standard notification callback could be triggered via main app coordinator
                }
            }, 300);
        });
    }
};

window.HelixSearch = HelixSearch;

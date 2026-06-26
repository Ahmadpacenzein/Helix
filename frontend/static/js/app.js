/* app.js - Unified dashboard load and event coordinator */

const App = {
    allEvents: [],
    currentCategoryFilters: [],
    currentDateFilter: null,
    searchQuery: '',

    /**
     * Initializes components and loads initial dashboard state.
     */
    async init() {
        try {
            // Bind App globally to support retry triggers from alerts
            window.App = this;

            // 1. Initialize UI components and callbacks
            HelixDashboard.init(
                (categories) => this.handleCategoryFilterChange(categories),
                (eventId) => this.handleEventSelection(eventId)
            );
            HelixTimelineSlider.init((date) => this.handleDateFilterChange(date));
            HelixSearch.init((results, query) => this.handleSearchCompleted(results, query));

            // 2. Initialize the map
            await HelixMap.init('map-container');

            // 3. Load database metrics and event logs
            await this.loadDashboardData();

        } catch (error) {
            console.error('App initialization error:', error);
            HelixDashboard.showAlert('Failed to initialize dashboard. Please check network and refresh.', 'danger');
        }
    },

    /**
     * Fetches dashboard datasets in parallel and renders components.
     */
    async loadDashboardData() {
        try {
            // Show loaders / spinner on sync indicator
            const syncSpinner = document.getElementById('sync-spinner');
            if (syncSpinner) {
                syncSpinner.classList.add('text-success');
                syncSpinner.classList.remove('text-muted');
                syncSpinner.style.animation = '';
            }

            const [summary, countryAnalytics, categoryAnalytics, syncStatus, events] = await Promise.all([
                HelixAPI.getDashboardSummary(),
                HelixAPI.getCountryAnalytics(),
                HelixAPI.getCategoryAnalytics(),
                HelixAPI.getSyncStatus(),
                HelixAPI.getEvents()
            ]);

            // Update UI components
            HelixDashboard.updateSummaryCards(summary);
            HelixDashboard.updateSyncLogs(syncStatus);
            HelixDashboard.renderCategoryFilters(categoryAnalytics);

            // Render Charts
            HelixCharts.renderCountryBar(countryAnalytics);
            HelixCharts.renderCategoryPie(categoryAnalytics);

            // Update event feed and map marker plots
            this.allEvents = events;
            HelixTimelineSlider.setEvents(events);
            this.applyFilters();

        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            HelixDashboard.showAlert(
                'Failed to load dashboard metrics. <a href="#" onclick="window.App.loadDashboardData(); return false;" class="alert-link fw-bold">Click here to retry</a>',
                'danger'
            );
        }
    },

    /**
     * Handles filter selection changes from category pills.
     */
    handleCategoryFilterChange(categories) {
        this.currentCategoryFilters = categories;
        this.applyFilters();
    },

    /**
     * Handles timeline range slider value updates.
     */
    handleDateFilterChange(date) {
        this.currentDateFilter = date;
        this.applyFilters();
    },

    /**
     * Integrates global search results list.
     */
    handleSearchCompleted(results, query) {
        this.searchQuery = query;
        this.allEvents = results;
        HelixTimelineSlider.setEvents(results);
        this.applyFilters();
    },

    /**
     * Event selection routing.
     */
    handleEventSelection(eventId) {
        HelixDashboard.renderEventDetail(eventId);
        HelixDashboard.highlightFeedItem(eventId);
    },

    /**
     * Applies compound filtering criteria and triggers UI updates.
     */
    applyFilters() {
        let filtered = this.allEvents;

        // 1. Filter by category tags
        if (this.currentCategoryFilters.length > 0) {
            filtered = filtered.filter(event => 
                event.category && this.currentCategoryFilters.includes(event.category.name)
            );
        }

        // 2. Filter by date slider
        if (this.currentDateFilter) {
            filtered = filtered.filter(event => 
                event.latest_geometry && 
                event.latest_geometry.date && 
                event.latest_geometry.date.startsWith(this.currentDateFilter)
            );
        }

        // 3. Render filtered items to Map, Feed and daily trend line chart
        HelixMap.renderEvents(filtered, (eventId) => this.handleEventSelection(eventId));
        HelixDashboard.renderLiveFeed(filtered.slice(0, 20));
        HelixCharts.renderDailyTrend(filtered);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

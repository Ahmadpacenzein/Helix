/* api.js - Central REST API communication module */

const API_BASE = '/api';

const HelixAPI = {
    /**
     * Fetch general dashboard metrics card counts.
     */
    async getDashboardSummary() {
        return this._fetchJson(`${API_BASE}/dashboard`);
    },

    /**
     * Fetch the list of disaster events.
     */
    async getEvents(filters = {}) {
        const params = new URLSearchParams();
        if (filters.country) params.append('country', filters.country);
        if (filters.category) params.append('category', filters.category);
        if (filters.status) params.append('status', filters.status);
        if (filters.date) params.append('date', filters.date);

        const url = `${API_BASE}/events${params.toString() ? '?' + params.toString() : ''}`;
        return this._fetchJson(url);
    },

    /**
     * Fetch details of a single event by ID.
     */
    async getEventDetail(eventId) {
        return this._fetchJson(`${API_BASE}/events/${eventId}`);
    },

    /**
     * Fetch aggregated statistics grouped by country.
     */
    async getCountryAnalytics() {
        return this._fetchJson(`${API_BASE}/analytics/country`);
    },

    /**
     * Fetch aggregated statistics grouped by category.
     */
    async getCategoryAnalytics() {
        return this._fetchJson(`${API_BASE}/analytics/category`);
    },

    /**
     * Search natural disaster events.
     */
    async searchEvents(query) {
        return this._fetchJson(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
    },

    /**
     * Fetch the timeline events feed.
     */
    async getTimeline() {
        return this._fetchJson(`${API_BASE}/timeline`);
    },

    /**
     * Fetch synchronization status logs.
     */
    async getSyncStatus() {
        return this._fetchJson(`${API_BASE}/sync/status`);
    },

    /**
     * Private helper to fetch JSON.
     */
    async _fetchJson(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const payload = await response.json();
            if (!payload.success) {
                throw new Error(payload.message || 'API request returned success: false');
            }
            return payload.data;
        } catch (error) {
            console.error(`API Fetch Error [${url}]:`, error);
            throw error;
        }
    }
};

window.HelixAPI = HelixAPI;

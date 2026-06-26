/* dashboard.js - UI component renders and dashboard status updates */

const HelixDashboard = {
    selectedCategories: new Set(),
    onCategoryFilterChanged: null,
    onEventSelected: null,

    /**
     * Initializes UI event listeners and selection handlers.
     */
    init(onCategoryFilterChanged, onEventSelected) {
        this.onCategoryFilterChanged = onCategoryFilterChanged;
        this.onEventSelected = onEventSelected;
    },

    /**
     * Updates counts on metric cards.
     */
    updateSummaryCards(summary) {
        document.getElementById('card-total-events').textContent = summary.total_events || 0;
        document.getElementById('card-active-events').textContent = summary.active_events || 0;
        document.getElementById('card-categories').textContent = summary.total_categories || 0;
        document.getElementById('card-countries').textContent = summary.total_countries || 0;
        document.getElementById('card-updated-today').textContent = summary.updated_today || 0;

        const syncTime = document.getElementById('sync-time');
        if (syncTime) {
            if (summary.last_sync) {
                const date = new Date(summary.last_sync);
                syncTime.textContent = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            } else {
                syncTime.textContent = 'None';
            }
        }
        
        const syncSpinner = document.getElementById('sync-spinner');
        if (syncSpinner) {
            syncSpinner.classList.remove('text-success');
            syncSpinner.classList.add('text-muted');
            syncSpinner.style.animation = 'none';
        }
    },

    /**
     * Refreshes synchronization status info panel.
     */
    updateSyncLogs(syncLog) {
        const insertEl = document.getElementById('sync-inserted');
        const updateEl = document.getElementById('sync-updated');
        const statusEl = document.getElementById('sync-status');
        const durationEl = document.getElementById('sync-duration');
        const idEl = document.getElementById('sync-id');

        if (insertEl) insertEl.textContent = syncLog.inserted ?? 0;
        if (updateEl) updateEl.textContent = syncLog.updated ?? 0;
        if (statusEl) {
            statusEl.textContent = syncLog.status || '-';
            statusEl.className = 'text-end fw-medium ' + (syncLog.status === 'Success' ? 'text-success' : 'text-danger');
        }
        if (durationEl) durationEl.textContent = syncLog.duration || '-';
        if (idEl) {
            idEl.textContent = syncLog.last_sync ? syncLog.last_sync.substring(0, 8) : '-';
            idEl.title = syncLog.last_sync || '';
        }
    },

    /**
     * Renders pills list in the category filter panel.
     */
    renderCategoryFilters(categories) {
        const container = document.getElementById('category-filter-list');
        if (!container) return;

        container.innerHTML = '';
        if (!categories || categories.length === 0) {
            container.innerHTML = '<span class="text-secondary small">No categories</span>';
            return;
        }

        categories.forEach(item => {
            const pill = document.createElement('span');
            pill.className = 'category-pill';
            pill.textContent = `${item.category} (${item.total_events})`;
            
            if (this.selectedCategories.has(item.category)) {
                pill.classList.add('active');
            }

            pill.addEventListener('click', () => {
                if (this.selectedCategories.has(item.category)) {
                    this.selectedCategories.delete(item.category);
                    pill.classList.remove('active');
                } else {
                    this.selectedCategories.add(item.category);
                    pill.classList.add('active');
                }

                if (this.onCategoryFilterChanged) {
                    this.onCategoryFilterChanged(Array.from(this.selectedCategories));
                }
            });

            container.appendChild(pill);
        });
    },

    /**
     * Renders recent events feed list.
     */
    renderLiveFeed(events) {
        const container = document.getElementById('live-feed-list');
        const countBadge = document.getElementById('feed-count');
        if (!container) return;

        container.innerHTML = '';
        if (countBadge) countBadge.textContent = events.length;

        if (!events || events.length === 0) {
            container.innerHTML = '<span class="text-secondary small text-center py-4">No events found</span>';
            return;
        }

        events.forEach(event => {
            const dateStr = event.latest_geometry && event.latest_geometry.date 
                ? event.latest_geometry.date.split('T')[0] 
                : 'N/A';
            
            const item = document.createElement('div');
            item.className = 'feed-item d-flex align-items-center justify-content-between';
            item.setAttribute('data-event-id', event.event_id);
            item.innerHTML = `
                <div class="text-truncate me-2">
                    <strong class="text-white d-block text-truncate small">${event.title}</strong>
                    <span class="text-secondary small" style="font-size: 0.75rem;">${event.category.name} | ${event.country || 'Global'}</span>
                </div>
                <div class="text-end flex-shrink-0">
                    <span class="badge bg-glass-badge text-secondary font-mono" style="font-size: 0.75rem;">${dateStr}</span>
                </div>
            `;

            item.addEventListener('click', () => {
                document.querySelectorAll('.feed-item').forEach(el => el.classList.remove('active'));
                item.classList.add('active');

                if (this.onEventSelected) {
                    this.onEventSelected(event.event_id);
                }
            });

            container.appendChild(item);
        });
    },

    /**
     * Loads and renders detailed info about a single event.
     */
    async renderEventDetail(eventId) {
        const contentArea = document.getElementById('detail-content');
        if (!contentArea) return;

        contentArea.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-info spinner-border-sm" role="status"></div>
                <span class="small ms-2">Loading details...</span>
            </div>
        `;

        try {
            const event = await HelixAPI.getEventDetail(eventId);
            if (!event) {
                contentArea.innerHTML = '<div class="text-center py-4 text-warning">Event details not found</div>';
                return;
            }

            const geom = event.latest_geometry || {};
            const lat = geom.latitude != null ? geom.latitude.toFixed(4) : 'N/A';
            const lng = geom.longitude != null ? geom.longitude.toFixed(4) : 'N/A';
            const dateStr = geom.date ? new Date(geom.date).toLocaleString() : 'N/A';

            contentArea.innerHTML = `
                <div class="detail-container text-white">
                    <h6 class="fw-bold text-white mb-2">${event.title}</h6>
                    <div class="d-flex gap-2 mb-3">
                        <span class="badge bg-primary-gradient small" style="font-size: 0.75rem;">${event.category.name}</span>
                        <span class="badge ${event.status === 'open' ? 'bg-success-gradient' : 'bg-secondary'} small" style="font-size: 0.75rem;">${event.status}</span>
                    </div>
                    <div class="detail-meta-item">
                        <span class="text-secondary d-block small">Country</span>
                        <span class="fw-medium">${event.country || 'Global / Open Ocean'}</span>
                    </div>
                    <div class="detail-meta-item">
                        <span class="text-secondary d-block small">Event Date</span>
                        <span class="fw-medium">${dateStr}</span>
                    </div>
                    <div class="detail-meta-item">
                        <span class="text-secondary d-block small">Coordinates</span>
                        <span class="fw-medium font-mono">${lat}°, ${lng}°</span>
                    </div>
                    ${event.sources && event.sources.length > 0 ? `
                    <div class="detail-meta-item">
                        <span class="text-secondary d-block small mb-1">Sources</span>
                        <div class="d-flex flex-wrap gap-1">
                            ${event.sources.map(src => `
                                <a href="${src.url}" target="_blank" class="badge bg-glass-badge text-decoration-none text-info py-1 px-2 border border-secondary" style="font-size: 0.7rem;">
                                    ${src.id} <i class="bi bi-box-arrow-up-right ms-1"></i>
                                </a>
                            `).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
            `;

            if (geom.longitude != null && geom.latitude != null) {
                HelixMap.flyTo(geom.longitude, geom.latitude, 5);
            }

        } catch (error) {
            console.error('Failed to load event details:', error);
            contentArea.innerHTML = '<div class="text-center py-4 text-danger">Failed to load event details.</div>';
        }
    },

    /**
     * Highlights feed item list programmatically.
     */
    highlightFeedItem(eventId) {
        document.querySelectorAll('.feed-item').forEach(el => {
            if (el.getAttribute('data-event-id') === eventId) {
                el.classList.add('active');
                el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                el.classList.remove('active');
            }
        });
    },

    /**
     * Displays a non-blocking error/info message.
     */
    showAlert(message, type = 'danger') {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show bg-glass text-white border-${type} shadow mb-3" role="alert">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill text-success' : 'bi-exclamation-triangle-fill text-danger'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        alertContainer.classList.remove('d-none');

        setTimeout(() => {
            const alertEl = alertContainer.querySelector('.alert');
            if (alertEl) {
                const bsAlert = new bootstrap.Alert(alertEl);
                bsAlert.close();
            }
        }, 5000);
    }
};

window.HelixDashboard = HelixDashboard;

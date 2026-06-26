/* charts.js - Analytics Charts rendering and management */

const HelixCharts = {
    categoryChart: null,
    countryChart: null,
    trendChart: null,

    /**
     * Renders Category Distribution (Pie Chart).
     */
    renderCategoryPie(data) {
        const ctx = document.getElementById('category-pie-chart');
        if (!ctx) return;

        if (this.categoryChart) {
            this.categoryChart.destroy();
        }

        const labels = data.map(item => item.category);
        const counts = data.map(item => item.total_events);

        const colors = [
            '#3b82f6', // blue
            '#ef4444', // red
            '#f59e0b', // yellow
            '#10b981', // green
            '#06b6d4', // cyan
            '#8b5cf6', // purple
            '#ec4899'  // pink
        ];

        this.categoryChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#a0aec0',
                            font: { family: 'Outfit', size: 11 }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(18, 19, 22, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                }
            }
        });
    },

    /**
     * Renders Country Aggregations (Bar Chart).
     */
    renderCountryBar(data) {
        const ctx = document.getElementById('country-bar-chart');
        if (!ctx) return;

        if (this.countryChart) {
            this.countryChart.destroy();
        }

        // Take top 5 countries
        const topData = data.slice(0, 5);
        const labels = topData.map(item => item.country || 'Unknown');
        const counts = topData.map(item => item.total_events);

        this.countryChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Events Count',
                    data: counts,
                    backgroundColor: 'rgba(59, 130, 246, 0.65)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(18, 19, 22, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: {
                            color: '#a0aec0',
                            font: { family: 'Outfit', size: 10 }
                        }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: {
                            color: '#a0aec0',
                            font: { family: 'Outfit', size: 10 },
                            precision: 0
                        }
                    }
                }
            }
        });
    },

    /**
     * Renders Daily Trend (Line Chart).
     */
    renderDailyTrend(events) {
        const ctx = document.getElementById('daily-trend-chart');
        if (!ctx) return;

        if (this.trendChart) {
            this.trendChart.destroy();
        }

        const dateCounts = {};
        events.forEach(event => {
            if (event.latest_geometry && event.latest_geometry.date) {
                const dateStr = event.latest_geometry.date.split('T')[0];
                dateCounts[dateStr] = (dateCounts[dateStr] || 0) + 1;
            }
        });

        const sortedDates = Object.keys(dateCounts).sort();
        const counts = sortedDates.map(d => dateCounts[d]);

        // Show last 10 days for a cleaner line chart view
        const displayDates = sortedDates.slice(-10);
        const displayCounts = counts.slice(-10);

        this.trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: displayDates,
                datasets: [{
                    label: 'Daily Count',
                    data: displayCounts,
                    fill: true,
                    backgroundColor: 'rgba(6, 182, 212, 0.15)',
                    borderColor: '#06b6d4',
                    borderWidth: 2,
                    tension: 0.3,
                    pointBackgroundColor: '#06b6d4'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(18, 19, 22, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: {
                            color: '#a0aec0',
                            font: { family: 'Outfit', size: 10 }
                        }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: {
                            color: '#a0aec0',
                            font: { family: 'Outfit', size: 10 },
                            precision: 0
                        }
                    }
                }
            }
        });
    }
};

window.HelixCharts = HelixCharts;

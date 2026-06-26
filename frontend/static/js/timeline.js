/* timeline.js - Range slider date filter control component */

const HelixTimelineSlider = {
    dates: [],
    isPlaying: false,
    playInterval: null,
    onDateChangedCallback: null,

    /**
     * Initializes the timeline slider listeners and state.
     * @param {Function} onDateChanged - Callback when slider selection updates.
     */
    init(onDateChanged) {
        this.onDateChangedCallback = onDateChanged;

        const slider = document.getElementById('timeline-slider');
        const playBtn = document.getElementById('play-timeline-btn');
        const resetBtn = document.getElementById('reset-timeline-btn');

        if (slider) {
            slider.addEventListener('input', (e) => {
                this.handleSliderChange(parseInt(e.target.value));
            });
        }

        if (playBtn) {
            playBtn.addEventListener('click', () => {
                if (this.isPlaying) {
                    this.pause();
                } else {
                    this.play();
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.reset();
            });
        }
    },

    /**
     * Updates dates scale from a refreshed list of events.
     * @param {Array} events - List of active events.
     */
    setEvents(events) {
        this.pause();

        const slider = document.getElementById('timeline-slider');
        const dateLabel = document.getElementById('selected-date-label');

        if (!events || events.length === 0) {
            this.dates = [];
            if (slider) {
                slider.min = 0;
                slider.max = 0;
                slider.value = 0;
                slider.disabled = true;
            }
            if (dateLabel) {
                dateLabel.textContent = 'No Dates';
            }
            return;
        }

        // Extract distinct sorted dates
        const dateSet = new Set();
        events.forEach(e => {
            if (e.latest_geometry && e.latest_geometry.date) {
                dateSet.add(e.latest_geometry.date.split('T')[0]);
            }
        });

        this.dates = Array.from(dateSet).sort();

        if (this.dates.length <= 1) {
            if (slider) {
                slider.min = 0;
                slider.max = 0;
                slider.value = 0;
                slider.disabled = true;
            }
            if (dateLabel) {
                dateLabel.textContent = this.dates[0] || 'All Dates';
            }
            return;
        }

        if (slider) {
            slider.disabled = false;
            slider.min = 0;
            slider.max = this.dates.length - 1;
            slider.value = this.dates.length - 1; // Default to latest date
        }

        if (dateLabel) {
            dateLabel.textContent = this.dates[this.dates.length - 1];
        }
    },

    /**
     * Handles slider index update.
     */
    handleSliderChange(index) {
        const dateLabel = document.getElementById('selected-date-label');
        if (index >= 0 && index < this.dates.length) {
            const selectedDate = this.dates[index];
            if (dateLabel) {
                dateLabel.textContent = selectedDate;
            }
            if (this.onDateChangedCallback) {
                this.onDateChangedCallback(selectedDate);
            }
        }
    },

    /**
     * Starts timeline play increment interval.
     */
    play() {
        const slider = document.getElementById('timeline-slider');
        if (!slider || slider.disabled || this.dates.length <= 1) return;

        this.isPlaying = true;
        const playBtn = document.getElementById('play-timeline-btn');
        if (playBtn) {
            playBtn.innerHTML = '<i class="bi bi-pause-fill text-white"></i>';
        }

        this.playInterval = setInterval(() => {
            let currentValue = parseInt(slider.value);
            let nextValue = currentValue + 1;
            if (nextValue >= this.dates.length) {
                nextValue = 0; // wrap around
            }
            slider.value = nextValue;
            this.handleSliderChange(nextValue);
        }, 1500);
    },

    /**
     * Pauses timeline increment interval.
     */
    pause() {
        this.isPlaying = false;
        const playBtn = document.getElementById('play-timeline-btn');
        if (playBtn) {
            playBtn.innerHTML = '<i class="bi bi-play-fill text-white"></i>';
        }
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
    },

    /**
     * Resets range slider to initial unselected state.
     */
    reset() {
        this.pause();
        const slider = document.getElementById('timeline-slider');
        const dateLabel = document.getElementById('selected-date-label');

        if (this.dates.length > 0) {
            if (slider) {
                slider.value = this.dates.length - 1;
            }
            if (dateLabel) {
                dateLabel.textContent = 'All Dates';
            }
            if (this.onDateChangedCallback) {
                this.onDateChangedCallback(null);
            }
        }
    }
};

window.HelixTimelineSlider = HelixTimelineSlider;

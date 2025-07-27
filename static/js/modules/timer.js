// Timer module for tracking response times

export class Timer {
    constructor(displayElement) {
        this.displayElement = displayElement;
        this.startTime = null;
        this.intervalId = null;
        this.elapsedSeconds = 0;
    }

    start() {
        this.stop(); // Clear any existing timer
        this.startTime = Date.now();
        this.elapsedSeconds = 0;
        this.updateDisplay();
        
        // Update every 100ms for smooth display
        this.intervalId = setInterval(() => {
            this.updateDisplay();
        }, 100);
    }

    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.updateDisplay();
    }

    reset() {
        this.stop();
        this.elapsedSeconds = 0;
        this.startTime = null;
        this.updateDisplay();
    }

    updateDisplay() {
        if (!this.displayElement) return;
        
        if (this.startTime) {
            const elapsed = Date.now() - this.startTime;
            this.elapsedSeconds = elapsed / 1000;
        }
        
        const seconds = Math.floor(this.elapsedSeconds);
        const tenths = Math.floor((this.elapsedSeconds % 1) * 10);
        
        // Format as SS.T
        const display = `${seconds}.${tenths}s`;
        this.displayElement.textContent = display;
    }

    getElapsedTime() {
        return this.elapsedSeconds;
    }
}
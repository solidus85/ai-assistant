// Status indicator module

export class StatusManager {
    constructor(statusDot, statusText, tokenLimit) {
        this.statusDot = statusDot;
        this.statusText = statusText;
        this.tokenLimit = tokenLimit;
    }

    updateStatus(data) {
        if (data.status === 'connected' && data.model_available) {
            this.statusDot.className = 'status-dot connected';
            this.statusText.textContent = 'Connected';
        } else if (data.status === 'connected') {
            this.statusDot.className = 'status-dot warning';
            this.statusText.textContent = 'Model not found';
        } else {
            this.statusDot.className = 'status-dot disconnected';
            this.statusText.textContent = 'Disconnected';
        }
        
        // Update token limit if available
        if (data.context_limit) {
            this.tokenLimit.textContent = data.context_limit;
        }
    }

    setError() {
        this.statusDot.className = 'status-dot disconnected';
        this.statusText.textContent = 'Connection error';
    }
}
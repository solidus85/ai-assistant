// Status indicator module

export class StatusManager {
    constructor(statusDot, statusText, tokenLimit) {
        this.statusDot = statusDot;
        this.statusText = statusText;
        this.tokenLimit = tokenLimit;
        this.modelName = null;
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
        
        // Store model name if available
        if (data.current_model) {
            this.modelName = data.current_model;
        }
    }

    setError() {
        this.statusDot.className = 'status-dot disconnected';
        this.statusText.textContent = 'Connection error';
    }
    
    getModelName() {
        return this.modelName;
    }
    
    formatModelName(modelName) {
        if (!modelName) return 'LLM';
        
        // Extract the base model name (before the colon)
        const baseName = modelName.split(':')[0];
        
        // Capitalize first letter
        return baseName.charAt(0).toUpperCase() + baseName.slice(1);
    }
}
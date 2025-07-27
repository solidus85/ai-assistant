// Token counter module

export class TokenManager {
    constructor(tokenCount, tokenLimit, tokenBarFill) {
        this.tokenCount = tokenCount;
        this.tokenLimit = tokenLimit;
        this.tokenBarFill = tokenBarFill;
    }

    updateTokenDisplay(data) {
        if (data.count !== undefined && data.limit !== undefined) {
            this.tokenCount.textContent = data.count;
            this.tokenLimit.textContent = data.limit;
            
            // Update progress bar
            const percentage = Math.min((data.count / data.limit) * 100, 100);
            this.tokenBarFill.style.width = percentage + '%';
            
            // Change color based on usage
            if (percentage > 90) {
                this.tokenBarFill.style.backgroundColor = '#e74c3c';
            } else if (percentage > 70) {
                this.tokenBarFill.style.backgroundColor = '#f39c12';
            } else {
                this.tokenBarFill.style.backgroundColor = '#3498db';
            }
        }
    }
}
// Global error handling utilities

export function setupGlobalErrorHandlers() {
    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        // Check if this is a browser extension error
        if (event.reason && event.reason.message) {
            const message = event.reason.message.toLowerCase();
            
            // Ignore common browser extension errors
            if (message.includes('message channel closed') ||
                message.includes('extension context invalidated') ||
                message.includes('receiving end does not exist')) {
                event.preventDefault(); // Prevent console error
                console.debug('Browser extension communication error (ignored):', event.reason.message);
                return;
            }
        }
        
        // Log other unhandled rejections
        console.error('Unhandled promise rejection:', event.reason);
    });
    
    // Handle global errors
    window.addEventListener('error', (event) => {
        // Check if this is a network error from extensions
        if (event.message && event.message.includes('Extension context')) {
            event.preventDefault();
            console.debug('Browser extension error (ignored):', event.message);
            return;
        }
        
        console.error('Global error:', event.error);
    });
}

// Wrap async functions to handle errors gracefully
export function wrapAsync(fn) {
    return async (...args) => {
        try {
            return await fn(...args);
        } catch (error) {
            // Check if it's an abort error (user cancelled)
            if (error.name === 'AbortError') {
                console.log('Operation cancelled by user');
                return;
            }
            
            // Check if it's a network timeout
            if (error.name === 'TimeoutError' || error.message.includes('timeout')) {
                console.warn('Operation timed out:', error.message);
                throw new Error('Request timed out. Please try again.');
            }
            
            // Re-throw other errors
            throw error;
        }
    };
}
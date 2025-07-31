// API communication module

export async function checkHealth() {
    const response = await fetch('/api/health');
    return await response.json();
}

export async function sendChatMessage(message, abortSignal, model = null) {
    // Create a timeout promise for very long responses (5 minutes)
    const timeoutMs = 300000; // 5 minutes
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => {
            reject(new Error(`Request timeout after ${timeoutMs/1000} seconds`));
        }, timeoutMs);
    });
    
    // Get selected model if not provided
    if (!model) {
        const modelSelect = document.getElementById('model-select');
        model = modelSelect ? modelSelect.value : null;
    }
    
    // Race between fetch and timeout
    const fetchPromise = fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: message,
            model: model
        }),
        signal: abortSignal
    });
    
    try {
        const response = await Promise.race([fetchPromise, timeoutPromise]);
        return response;
    } catch (error) {
        if (error.message.includes('timeout')) {
            // Create a custom timeout error
            const timeoutError = new Error('Response took too long. Please try with a shorter prompt or use the stop button.');
            timeoutError.name = 'TimeoutError';
            throw timeoutError;
        }
        throw error;
    }
}

export async function clearConversation(sessionId) {
    const response = await fetch('/api/conversation/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId })
    });
    return response;
}

export async function getTokenCount(message) {
    const response = await fetch('/api/chat/tokens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message || ''
        })
    });
    return await response.json();
}
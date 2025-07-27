// API communication module

export async function checkHealth() {
    const response = await fetch('/api/health');
    return await response.json();
}

export async function sendChatMessage(message) {
    const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: message
        })
    });
    return response;
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
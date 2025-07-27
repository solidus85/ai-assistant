// Local storage utility functions

export function getSessionId() {
    return localStorage.getItem('chat-session-id');
}

export function setSessionId(sessionId) {
    localStorage.setItem('chat-session-id', sessionId);
}

export function getShowPrompts() {
    return localStorage.getItem('show-prompts') === 'true';
}

export function setShowPrompts(show) {
    localStorage.setItem('show-prompts', show);
}
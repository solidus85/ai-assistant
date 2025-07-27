// Chat functionality module

import { escapeHtml, createElement, scrollToBottom } from '../utils/dom.js';
import { sendChatMessage } from './api.js';

export class ChatManager {
    constructor(outputArea, userInput, sendButton) {
        this.outputArea = outputArea;
        this.userInput = userInput;
        this.sendButton = sendButton;
        this.abortController = null;
    }

    addUserMessage(message) {
        // Clear the output area for each new request
        this.outputArea.innerHTML = '';
        
        const userMessageDiv = createElement('div', 'message user-message', 
            `<strong>You:</strong> <span class="user-content">${escapeHtml(message)}</span>`);
        this.outputArea.appendChild(userMessageDiv);
    }

    createAssistantMessageContainer() {
        const responseContainer = createElement('div', 'message assistant-message',
            `<strong>Assistant:</strong> 
            <span class="message-loading">
                <span>Thinking</span>
                <span class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </span>
            </span>
            <span id="streaming-response" class="response" style="display: none;"></span>`);
        this.outputArea.appendChild(responseContainer);
        return document.getElementById('streaming-response');
    }

    async streamResponse(message, onPromptDisplay, responseTime) {
        // Create new abort controller for this request
        this.abortController = new AbortController();
        
        try {
            const response = await sendChatMessage(message, this.abortController.signal);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let totalChars = 0;
            let tokenCount = 0;

            while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.trim()) {
                    try {
                        const data = JSON.parse(line);
                        
                        if (data.error) {
                            this.displayError(data.error);
                            return;
                        }
                        
                        if (data.token) {
                            const streamingSpan = document.getElementById('streaming-response');
                            
                            // Hide loading indicator on first token
                            if (tokenCount === 0) {
                                const loadingSpan = streamingSpan.parentElement.querySelector('.message-loading');
                                if (loadingSpan) {
                                    loadingSpan.style.display = 'none';
                                }
                                streamingSpan.style.display = 'inline';
                            }
                            
                            streamingSpan.textContent += data.token;
                            totalChars += data.token.length;
                            tokenCount++;
                        }
                        
                        if (data.done && data.total_time) {
                            console.log(`Response time: ${data.total_time.toFixed(2)}s`);
                            console.log(`Total response length: ${totalChars} characters, ${tokenCount} tokens`);
                            if (data.eval_count) {
                                console.log(`Model reported ${data.eval_count} tokens generated`);
                            }
                            
                            // Add response time to the message
                            if (responseTime) {
                                const timeDiv = createElement('div', 'response-time', 
                                    `Response time: ${responseTime.toFixed(1)}s`);
                                document.getElementById('streaming-response').parentElement.appendChild(timeDiv);
                            }
                        }
                        
                        if (data.full_prompt) {
                            onPromptDisplay(data.full_prompt);
                        }
                    } catch (e) {
                        console.error('Failed to parse line:', line);
                    }
                }
            }
        }
        } catch (error) {
            if (error.name === 'AbortError') {
                // Add a message indicating the response was stopped
                const streamingSpan = document.getElementById('streaming-response');
                if (streamingSpan) {
                    streamingSpan.innerHTML += '<span class="response-stopped"> [Response stopped by user]</span>';
                }
                console.log('Response generation stopped by user');
            } else {
                throw error;
            }
        } finally {
            this.abortController = null;
        }
    }

    displayError(error) {
        const errorDiv = createElement('div', 'error', `Error: ${escapeHtml(error)}`);
        this.outputArea.appendChild(errorDiv);
    }

    clearOutput() {
        this.outputArea.innerHTML = '<p class="welcome-message">Output cleared. Ask me anything...</p>';
    }

    enableInput() {
        this.userInput.disabled = false;
        this.userInput.focus();
        this.sendButton.disabled = false;
    }

    disableInput() {
        this.sendButton.disabled = true;
        this.userInput.disabled = true;
    }

    scrollToBottom() {
        scrollToBottom(this.outputArea);
    }
    
    stopResponse() {
        if (this.abortController) {
            this.abortController.abort();
            return true;
        }
        return false;
    }
    
    isStreaming() {
        return this.abortController !== null;
    }
}
// Chat functionality module

import { escapeHtml, createElement, scrollToBottom } from '../utils/dom.js';
import { sendChatMessage } from './api.js';

export class ChatManager {
    constructor(outputArea, userInput, sendButton) {
        this.outputArea = outputArea;
        this.userInput = userInput;
        this.sendButton = sendButton;
    }

    addUserMessage(message) {
        // Clear the output area for each new request
        this.outputArea.innerHTML = '';
        
        const userMessageDiv = createElement('div', 'message user-message', 
            `<strong>You:</strong> ${message}`);
        this.outputArea.appendChild(userMessageDiv);
    }

    createAssistantMessageContainer() {
        const responseContainer = createElement('div', 'message assistant-message',
            '<strong>Assistant:</strong> <span id="streaming-response" class="response"></span>');
        this.outputArea.appendChild(responseContainer);
        return document.getElementById('streaming-response');
    }

    async streamResponse(message, onPromptDisplay) {
        const response = await sendChatMessage(message);
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
                            document.getElementById('streaming-response').textContent += data.token;
                            totalChars += data.token.length;
                            tokenCount++;
                        }
                        
                        if (data.done && data.total_time) {
                            console.log(`Response time: ${data.total_time.toFixed(2)}s`);
                            console.log(`Total response length: ${totalChars} characters, ${tokenCount} tokens`);
                            if (data.eval_count) {
                                console.log(`Model reported ${data.eval_count} tokens generated`);
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
}
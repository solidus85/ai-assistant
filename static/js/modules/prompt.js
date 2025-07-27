// Prompt display module

import { escapeHtml, createElement } from '../utils/dom.js';

export class PromptManager {
    constructor(outputArea, toggleButton) {
        this.outputArea = outputArea;
        this.toggleButton = toggleButton;
        this.showPrompts = false;
    }

    setShowPrompts(show) {
        this.showPrompts = show;
        this.toggleButton.textContent = show ? 'Hide Prompt' : 'Show Prompt';
    }

    toggle() {
        this.setShowPrompts(!this.showPrompts);
        
        // Hide existing prompt displays if turning off
        if (!this.showPrompts) {
            document.querySelectorAll('.prompt-display').forEach(el => el.remove());
        } else {
            // Show info message if no messages yet
            if (this.outputArea.querySelectorAll('.message').length === 0) {
                this.showInfoMessage();
            }
        }
        
        return this.showPrompts;
    }

    showInfoMessage() {
        const infoDiv = createElement('div', 'prompt-display', `
            <div class="prompt-header">
                <strong>Prompt Display Enabled</strong>
            </div>
            <div class="prompt-content">
                Send a new message to see the full prompt that will be sent to the model.
                The prompt includes all conversation history.
            </div>
        `);
        this.outputArea.appendChild(infoDiv);
    }

    displayPrompt(prompt) {
        if (!this.showPrompts) return;

        const promptDiv = createElement('div', 'prompt-display', `
            <div class="prompt-header">
                <strong>Full Prompt Sent to Model:</strong>
                <button class="copy-prompt" onclick="window.copyPrompt(this)">Copy</button>
            </div>
            <pre class="prompt-content">${escapeHtml(prompt)}</pre>
        `);
        
        // Insert after the last user message (before assistant message)
        const messages = this.outputArea.querySelectorAll('.message');
        if (messages.length >= 2) {
            const lastUserMessage = messages[messages.length - 2];
            lastUserMessage.after(promptDiv);
        } else if (messages.length === 1) {
            messages[0].after(promptDiv);
        } else {
            this.outputArea.appendChild(promptDiv);
        }
    }
}

// Global function for copy button
window.copyPrompt = function(button) {
    const promptContent = button.parentElement.nextElementSibling.textContent;
    navigator.clipboard.writeText(promptContent).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => button.textContent = 'Copy', 2000);
    });
}
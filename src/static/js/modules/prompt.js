// Prompt display module

import { escapeHtml, createElement } from '../utils/dom.js';

export class PromptManager {
    constructor(consoleOutput, toggleButton, consolePanel) {
        this.consoleOutput = consoleOutput;
        this.toggleButton = toggleButton;
        this.consolePanel = consolePanel;
        this.showConsole = false;
    }

    setShowConsole(show) {
        this.showConsole = show;
        this.toggleButton.textContent = show ? 'Hide Console' : 'Show Console';
        
        if (show) {
            this.consolePanel.classList.remove('hidden');
        } else {
            this.consolePanel.classList.add('hidden');
        }
    }

    toggle() {
        this.setShowConsole(!this.showConsole);
        return this.showConsole;
    }

    displayPrompt(prompt) {
        // Remove welcome message if it exists
        const welcomeMsg = this.consoleOutput.querySelector('.console-welcome');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        // Create timestamp
        const timestamp = new Date().toLocaleTimeString();
        
        const promptEntry = createElement('div', 'console-entry', `
            <div class="console-entry-header">
                <span class="console-entry-time">${timestamp}</span>
                <button class="copy-console-prompt" onclick="window.copyConsolePrompt(this)">Copy</button>
            </div>
            <pre class="console-entry-content">${escapeHtml(prompt)}</pre>
        `);
        
        // Add to console output
        this.consoleOutput.appendChild(promptEntry);
        
        // Auto-scroll to bottom
        this.consoleOutput.scrollTop = this.consoleOutput.scrollHeight;
        
        // Auto-show console if hidden
        if (!this.showConsole) {
            this.setShowConsole(true);
        }
    }
    
    clearConsole() {
        this.consoleOutput.innerHTML = '<p class="console-welcome">Prompts will appear here when you send messages...</p>';
    }
}

// Global function for copy button
window.copyConsolePrompt = function(button) {
    const promptContent = button.parentElement.nextElementSibling.textContent;
    navigator.clipboard.writeText(promptContent).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => button.textContent = originalText, 2000);
    });
}
// Parse module

export class ParseManager {
    constructor(elements) {
        this.parseInput = elements.parseInput;
        this.parseOutput = elements.parseOutput;
        this.parseButton = elements.parseButton;
        this.parseStopButton = elements.parseStopButton;
        this.parseClearButton = elements.parseClearButton;
        this.abortController = null;
    }

    setupEventListeners() {
        this.parseButton.addEventListener('click', () => this.handleParse());
        this.parseStopButton.addEventListener('click', () => this.handleStop());
        this.parseClearButton.addEventListener('click', () => this.clearOutput());
        
        this.parseInput.addEventListener('input', () => {
            this.parseButton.disabled = this.parseInput.value.trim() === '';
        });
        
        this.parseInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!this.parseButton.disabled) {
                    this.handleParse();
                }
            }
        });
    }

    async handleParse() {
        const text = this.parseInput.value.trim();
        if (!text) return;

        this.disableInput();
        this.addUserMessage(text);
        
        // Clear input
        this.parseInput.value = '';
        
        // Show stop button, hide parse button
        this.parseButton.style.display = 'none';
        this.parseStopButton.style.display = 'flex';
        
        // Add response container
        const responseDiv = this.createAssistantMessageContainer();

        try {
            this.abortController = new AbortController();
            
            const response = await fetch('/api/parse/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
                signal: this.abortController.signal
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            if (data.content) {
                                this.appendToResponse(responseDiv, data.content);
                            }
                            if (data.error) {
                                this.displayError(data.error);
                            }
                        } catch (e) {
                            console.error('Failed to parse JSON:', e);
                        }
                    }
                }
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                this.appendToResponse(responseDiv, '\n\n[Response stopped by user]');
            } else {
                this.displayError('Failed to connect to server');
            }
        } finally {
            // Hide stop button, show parse button
            this.parseStopButton.style.display = 'none';
            this.parseButton.style.display = 'block';
            
            this.enableInput();
            this.scrollToBottom();
            this.abortController = null;
        }
    }

    handleStop() {
        if (this.abortController) {
            this.abortController.abort();
        }
    }

    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `<strong>Input:</strong><br><span class="user-content">${this.escapeHtml(message)}</span>`;
        this.parseOutput.appendChild(messageDiv);
        this.scrollToBottom();
    }

    createAssistantMessageContainer() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant-message';
        messageDiv.innerHTML = '<strong>Parsed Result:</strong><br><span class="response"></span>';
        this.parseOutput.appendChild(messageDiv);
        return messageDiv.querySelector('.response');
    }

    appendToResponse(responseElement, content) {
        responseElement.textContent += content;
        this.scrollToBottom();
    }

    displayError(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = `Error: ${error}`;
        this.parseOutput.appendChild(errorDiv);
        this.scrollToBottom();
    }

    clearOutput() {
        this.parseOutput.innerHTML = '<p class="welcome-message">Welcome to Parse! Paste your text to parse...</p>';
        this.parseInput.focus();
    }

    disableInput() {
        this.parseInput.disabled = true;
        this.parseButton.disabled = true;
    }

    enableInput() {
        this.parseInput.disabled = false;
        this.parseButton.disabled = this.parseInput.value.trim() === '';
        this.parseInput.focus();
    }

    scrollToBottom() {
        this.parseOutput.scrollTop = this.parseOutput.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}
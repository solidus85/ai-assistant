// Summarization module

import { escapeHtml, createElement } from '../utils/dom.js';

export class SummarizeManager {
    constructor(elements) {
        this.input = elements.summarizeInput;
        this.output = elements.summarizeOutput;
        this.button = elements.summarizeButton;
        this.clearButton = elements.clearSummarizeButton;
        this.tokenCount = elements.summarizeTokenCount;
        this.tokenLimit = elements.summarizeTokenLimit;
    }

    setupEventListeners() {
        // Enable/disable button based on input
        this.input.addEventListener('input', () => {
            this.button.disabled = this.input.value.trim() === '';
            this.updateTokenCount();
        });

        // Summarize button click
        this.button.addEventListener('click', () => {
            this.summarize();
        });

        // Clear button click
        this.clearButton.addEventListener('click', () => {
            this.clear();
        });

        // Ctrl/Cmd + Enter to summarize
        this.input.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                if (!this.button.disabled) {
                    this.summarize();
                }
            }
        });
    }

    async summarize() {
        const text = this.input.value.trim();
        if (!text) return;

        // Disable controls
        this.button.disabled = true;
        this.input.disabled = true;

        // Show loading state
        this.output.innerHTML = '<div class="summarize-result loading">Summarizing with Phi3:mini...</div>';

        try {
            const response = await fetch('/api/summarize/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let summaryText = '';

            // Clear output and prepare for streaming
            this.output.innerHTML = '<div class="summarize-result"></div>';
            const resultDiv = this.output.querySelector('.summarize-result');

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
                                summaryText += data.token;
                                resultDiv.textContent = summaryText;
                            }
                            
                            if (data.done && data.total_time) {
                                console.log(`Summarization time: ${data.total_time.toFixed(2)}s using ${data.model}`);
                            }
                        } catch (e) {
                            console.error('Failed to parse line:', line);
                        }
                    }
                }
            }
        } catch (error) {
            this.displayError('Failed to connect to summarization service');
        }

        // Re-enable controls
        this.input.disabled = false;
        this.button.disabled = false;
        this.input.focus();
    }

    displayError(error) {
        this.output.innerHTML = `<div class="summarize-result error">Error: ${escapeHtml(error)}</div>`;
    }

    clear() {
        this.input.value = '';
        this.output.innerHTML = '<p class="summarize-welcome">Your summary will appear here...</p>';
        this.button.disabled = true;
        this.updateTokenCount();
        this.input.focus();
    }

    async updateTokenCount() {
        try {
            const response = await fetch('/api/summarize/tokens', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: this.input.value || ''
                })
            });
            
            const data = await response.json();
            
            if (data.count !== undefined) {
                this.tokenCount.textContent = data.count;
                
                // Change color based on usage
                const percentage = (data.count / data.limit) * 100;
                if (percentage > 90) {
                    this.tokenCount.style.color = 'var(--accent-error)';
                } else if (percentage > 70) {
                    this.tokenCount.style.color = 'var(--accent-warning)';
                } else {
                    this.tokenCount.style.color = 'var(--text-secondary)';
                }
            }
        } catch (error) {
            console.error('Failed to update token count:', error);
        }
    }
}
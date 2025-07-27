// Summarization system prompt management module

export class SummarizeSystemPromptManager {
    constructor(promptElement, saveButton) {
        this.promptElement = promptElement;
        this.saveButton = saveButton;
        this.originalPrompt = '';
    }

    async loadSystemPrompt() {
        try {
            const response = await fetch('/api/settings/summarize-system-prompt');
            const data = await response.json();
            
            if (data.system_prompt !== undefined) {
                this.promptElement.value = data.system_prompt;
                this.originalPrompt = data.system_prompt;
                this.updateSaveButtonState();
            }
        } catch (error) {
            console.error('Failed to load summarization system prompt:', error);
        }
    }

    setupEventListeners() {
        // Track changes
        this.promptElement.addEventListener('input', () => {
            this.updateSaveButtonState();
        });

        // Save button click
        this.saveButton.addEventListener('click', () => {
            this.saveSystemPrompt();
        });

        // Keyboard shortcut (Ctrl/Cmd + S)
        this.promptElement.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                if (!this.saveButton.disabled) {
                    this.saveSystemPrompt();
                }
            }
        });
    }

    updateSaveButtonState() {
        const hasChanged = this.promptElement.value !== this.originalPrompt;
        this.saveButton.disabled = !hasChanged;
        
        if (hasChanged) {
            this.saveButton.classList.add('unsaved');
            this.saveButton.textContent = 'Save*';
        } else {
            this.saveButton.classList.remove('unsaved');
            this.saveButton.textContent = 'Save';
        }
    }

    async saveSystemPrompt() {
        const newPrompt = this.promptElement.value;
        
        try {
            this.saveButton.disabled = true;
            this.saveButton.textContent = 'Saving...';
            
            const response = await fetch('/api/settings/summarize-system-prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ system_prompt: newPrompt })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.originalPrompt = newPrompt;
                this.saveButton.textContent = 'Saved!';
                this.saveButton.classList.add('saved');
                
                setTimeout(() => {
                    this.saveButton.classList.remove('saved');
                    this.updateSaveButtonState();
                }, 2000);
            } else {
                throw new Error(data.message || 'Failed to save');
            }
        } catch (error) {
            console.error('Failed to save summarization system prompt:', error);
            this.saveButton.textContent = 'Error!';
            this.saveButton.classList.add('error');
            
            setTimeout(() => {
                this.saveButton.classList.remove('error');
                this.updateSaveButtonState();
            }, 2000);
        }
    }
}
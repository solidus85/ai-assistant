// System prompt management module

export class SystemPromptManager {
    constructor(promptTextarea, saveButton) {
        this.promptTextarea = promptTextarea;
        this.saveButton = saveButton;
        this.originalPrompt = '';
    }

    async loadSystemPrompt() {
        try {
            const response = await fetch('/api/settings/system-prompt');
            const data = await response.json();
            
            if (data.system_prompt !== undefined) {
                this.promptTextarea.value = data.system_prompt;
                this.originalPrompt = data.system_prompt;
                this.updateSaveButtonState();
            }
        } catch (error) {
            console.error('Failed to load system prompt:', error);
        }
    }

    async saveSystemPrompt() {
        const newPrompt = this.promptTextarea.value.trim();
        
        try {
            const response = await fetch('/api/settings/system-prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    system_prompt: newPrompt
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.originalPrompt = newPrompt;
                this.updateSaveButtonState();
                this.showSaveSuccess();
            } else {
                console.error('Failed to save system prompt');
            }
        } catch (error) {
            console.error('Failed to save system prompt:', error);
        }
    }

    updateSaveButtonState() {
        const currentValue = this.promptTextarea.value.trim();
        const hasChanged = currentValue !== this.originalPrompt;
        
        this.saveButton.disabled = !hasChanged;
        this.saveButton.textContent = hasChanged ? 'Save' : 'Saved';
        
        // Update button style based on state
        if (hasChanged) {
            this.saveButton.classList.add('unsaved');
        } else {
            this.saveButton.classList.remove('unsaved');
        }
    }

    showSaveSuccess() {
        const originalText = this.saveButton.textContent;
        this.saveButton.textContent = 'Saved!';
        this.saveButton.classList.add('success');
        
        setTimeout(() => {
            this.saveButton.classList.remove('success');
            this.updateSaveButtonState();
        }, 2000);
    }

    setupEventListeners() {
        // Update save button state when text changes
        this.promptTextarea.addEventListener('input', () => {
            this.updateSaveButtonState();
        });
        
        // Save on button click
        this.saveButton.addEventListener('click', () => {
            this.saveSystemPrompt();
        });
        
        // Save on Ctrl+S / Cmd+S
        this.promptTextarea.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                if (!this.saveButton.disabled) {
                    this.saveSystemPrompt();
                }
            }
        });
    }
}
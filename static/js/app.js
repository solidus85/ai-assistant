// Main application entry point

import { getShowPrompts, setShowPrompts } from './utils/storage.js';
import { checkHealth, clearConversation, getTokenCount } from './modules/api.js';
import { StatusManager } from './modules/status.js';
import { TokenManager } from './modules/tokens.js';
import { ChatManager } from './modules/chat.js';
import { PromptManager } from './modules/prompt.js';
import { TabManager } from './modules/tabs.js';
import { ParseManager } from './modules/parse.js';
import { Timer } from './modules/timer.js';
import { setupGlobalErrorHandlers } from './utils/error-handler.js';

// Setup global error handlers
setupGlobalErrorHandlers();

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const elements = {
        userInput: document.getElementById('user-input'),
        sendButton: document.getElementById('send-button'),
        stopButton: document.getElementById('stop-button'),
        clearButton: document.getElementById('clear-button'),
        togglePromptButton: document.getElementById('toggle-prompt'),
        outputArea: document.getElementById('output'),
        statusDot: document.getElementById('status-dot'),
        statusText: document.getElementById('status-text'),
        tokenCount: document.getElementById('token-count'),
        tokenLimit: document.getElementById('token-limit'),
        tokenBarFill: document.getElementById('token-bar-fill'),
        consolePanel: document.getElementById('console-panel'),
        consoleOutput: document.getElementById('console-output'),
        clearConsoleButton: document.getElementById('clear-console'),
        // Parse tab elements
        parseInput: document.getElementById('parse-input'),
        parseOutput: document.getElementById('parse-output'),
        parseButton: document.getElementById('parse-button'),
        parseStopButton: document.getElementById('parse-stop-button'),
        parseClearButton: document.getElementById('parse-clear-button'),
        // Progress indicator elements
        progressContainer: document.getElementById('progress-container'),
        timerDisplay: document.getElementById('timer-display')
    };

    
    // Initialize managers
    const statusManager = new StatusManager(
        elements.statusDot, 
        elements.statusText, 
        elements.tokenLimit
    );
    
    const tokenManager = new TokenManager(
        elements.tokenCount,
        elements.tokenLimit,
        elements.tokenBarFill
    );
    
    const chatManager = new ChatManager(
        elements.outputArea,
        elements.userInput,
        elements.sendButton
    );
    
    const promptManager = new PromptManager(
        elements.consoleOutput,
        elements.togglePromptButton,
        elements.consolePanel
    );
    
    const tabManager = new TabManager();
    
    const parseManager = new ParseManager({
        parseInput: elements.parseInput,
        parseOutput: elements.parseOutput,
        parseButton: elements.parseButton,
        parseStopButton: elements.parseStopButton,
        parseClearButton: elements.parseClearButton
    });
    
    const timer = new Timer(elements.timerDisplay);

    // Initialize console state
    promptManager.setShowConsole(getShowPrompts());
    
    // Setup tab navigation
    tabManager.setupEventListeners();
    
    // Setup parse functionality
    parseManager.setupEventListeners();

    // Check health and update tokens on load
    performHealthCheck();
    updateTokenCount();

    // Event listeners
    elements.sendButton.addEventListener('click', sendMessage);
    elements.stopButton.addEventListener('click', handleStopResponse);
    elements.clearButton.addEventListener('click', handleClearConversation);
    elements.togglePromptButton.addEventListener('click', handleTogglePrompt);
    elements.clearConsoleButton.addEventListener('click', handleClearConsole);
    
    elements.userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    elements.userInput.addEventListener('input', () => {
        elements.sendButton.disabled = elements.userInput.value.trim() === '';
        updateTokenCount();
    });

    // Functions
    async function performHealthCheck() {
        try {
            const data = await checkHealth();
            statusManager.updateStatus(data);
            
        } catch (error) {
            statusManager.setError();
        }
    }

    async function sendMessage() {
        const message = elements.userInput.value.trim();
        if (!message) return;

        chatManager.disableInput();
        chatManager.addUserMessage(message);
        
        // Clear input
        elements.userInput.value = '';
        
        // Show progress indicator and start timer
        elements.progressContainer.classList.add('active');
        timer.start();
        
        // Show stop button, hide send button
        elements.sendButton.style.display = 'none';
        elements.stopButton.style.display = 'flex';
        
        // Add response container
        const responseDiv = chatManager.createAssistantMessageContainer();

        try {
            await chatManager.streamResponse(
                message,
                (fullPrompt) => {
                    promptManager.displayPrompt(fullPrompt);
                },
                timer.getElapsedTime()
            );
        } catch (error) {
            chatManager.displayError('Failed to connect to server');
        }

        // Stop timer and hide progress indicator
        timer.stop();
        elements.progressContainer.classList.remove('active');
        
        // Hide stop button, show send button
        elements.stopButton.style.display = 'none';
        elements.sendButton.style.display = 'block';
        
        chatManager.enableInput();
        chatManager.scrollToBottom();
        
        // Update token count after message sent
        setTimeout(updateTokenCount, 100);
    }

    async function handleClearConversation() {
        // Clear the output area
        chatManager.clearOutput();
        elements.userInput.focus();
        updateTokenCount();
    }
    
    function handleStopResponse() {
        if (chatManager.stopResponse()) {
            // Stop timer and hide progress indicator
            timer.stop();
            elements.progressContainer.classList.remove('active');
            
            // Hide stop button, show send button
            elements.stopButton.style.display = 'none';
            elements.sendButton.style.display = 'block';
            
            // Re-enable input
            chatManager.enableInput();
            
            // Update token count
            setTimeout(updateTokenCount, 100);
        }
    }

    function handleTogglePrompt() {
        const showConsole = promptManager.toggle();
        setShowPrompts(showConsole);
    }
    
    function handleClearConsole() {
        promptManager.clearConsole();
    }

    async function updateTokenCount() {
        try {
            const data = await getTokenCount(elements.userInput.value);
            tokenManager.updateTokenDisplay(data);
        } catch (error) {
            console.error('Failed to update token count:', error);
        }
    }

    // Periodic health check
    setInterval(performHealthCheck, 30000);
});
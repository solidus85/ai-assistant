// Main application entry point

import { getShowPrompts, setShowPrompts } from './utils/storage.js';
import { checkHealth, clearConversation, getTokenCount } from './modules/api.js';
import { StatusManager } from './modules/status.js';
import { TokenManager } from './modules/tokens.js';
import { ChatManager } from './modules/chat.js';
import { PromptManager } from './modules/prompt.js';
import { SystemPromptManager } from './modules/system-prompt.js';
import { TabManager } from './modules/tabs.js';
import { SummarizeManager } from './modules/summarize.js';
import { SummarizeSystemPromptManager } from './modules/summarize-system-prompt.js';

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const elements = {
        userInput: document.getElementById('user-input'),
        sendButton: document.getElementById('send-button'),
        clearButton: document.getElementById('clear-button'),
        togglePromptButton: document.getElementById('toggle-prompt'),
        outputArea: document.getElementById('output'),
        statusDot: document.getElementById('status-dot'),
        statusText: document.getElementById('status-text'),
        tokenCount: document.getElementById('token-count'),
        tokenLimit: document.getElementById('token-limit'),
        tokenBarFill: document.getElementById('token-bar-fill'),
        systemPrompt: document.getElementById('system-prompt'),
        savePromptButton: document.getElementById('save-prompt'),
        consolePanel: document.getElementById('console-panel'),
        consoleOutput: document.getElementById('console-output'),
        clearConsoleButton: document.getElementById('clear-console'),
        // Summarize tab elements
        summarizeInput: document.getElementById('summarize-input'),
        summarizeOutput: document.getElementById('summarize-output'),
        summarizeButton: document.getElementById('summarize-button'),
        clearSummarizeButton: document.getElementById('clear-summarize'),
        summarizeTokenCount: document.getElementById('summarize-token-count'),
        summarizeTokenLimit: document.getElementById('summarize-token-limit'),
        summarizeSystemPrompt: document.getElementById('summarize-system-prompt'),
        saveSummarizePromptButton: document.getElementById('save-summarize-prompt')
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
    
    const systemPromptManager = new SystemPromptManager(
        elements.systemPrompt,
        elements.savePromptButton
    );
    
    const tabManager = new TabManager();
    
    const summarizeManager = new SummarizeManager({
        summarizeInput: elements.summarizeInput,
        summarizeOutput: elements.summarizeOutput,
        summarizeButton: elements.summarizeButton,
        clearSummarizeButton: elements.clearSummarizeButton,
        summarizeTokenCount: elements.summarizeTokenCount,
        summarizeTokenLimit: elements.summarizeTokenLimit
    });
    
    const summarizeSystemPromptManager = new SummarizeSystemPromptManager(
        elements.summarizeSystemPrompt,
        elements.saveSummarizePromptButton
    );

    // Initialize console state
    promptManager.setShowConsole(getShowPrompts());
    
    // Load and setup system prompt
    systemPromptManager.loadSystemPrompt();
    systemPromptManager.setupEventListeners();
    
    // Setup tab navigation
    tabManager.setupEventListeners();
    
    // Setup summarization
    summarizeManager.setupEventListeners();
    
    // Load and setup summarize system prompt
    summarizeSystemPromptManager.loadSystemPrompt();
    summarizeSystemPromptManager.setupEventListeners();

    // Check health and update tokens on load
    performHealthCheck();
    updateTokenCount();

    // Event listeners
    elements.sendButton.addEventListener('click', sendMessage);
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
            
            // Update page title and header with model name
            if (data.current_model) {
                const formattedName = statusManager.formatModelName(data.current_model);
                document.title = `${formattedName} Chat Interface`;
                const chatTitle = document.getElementById('chat-title');
                if (chatTitle) {
                    chatTitle.textContent = `${formattedName} Chat`;
                }
            }
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
        
        // Add response container
        const responseDiv = chatManager.createAssistantMessageContainer();

        try {
            await chatManager.streamResponse(
                message,
                (fullPrompt) => {
                    promptManager.displayPrompt(fullPrompt);
                }
            );
        } catch (error) {
            chatManager.displayError('Failed to connect to server');
        }

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
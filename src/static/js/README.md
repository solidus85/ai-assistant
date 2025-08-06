# JavaScript Module Structure

The JavaScript code has been modularized for better maintainability and organization.

## Directory Structure

```
js/
├── app.js              # Main entry point - initializes and coordinates all modules
├── modules/            # Feature-specific modules
│   ├── api.js         # API communication functions
│   ├── chat.js        # Chat UI and message handling
│   ├── prompt.js      # Prompt display functionality
│   ├── status.js      # Connection status management
│   └── tokens.js      # Token counter management
└── utils/             # Utility functions
    ├── dom.js         # DOM manipulation helpers
    └── storage.js     # Local storage helpers
```

## Module Descriptions

### Main Application (app.js)
- Initializes all managers on DOM load
- Sets up event listeners
- Coordinates between different modules
- Manages periodic health checks

### Modules

#### api.js
- `checkHealth()` - Check Ollama connection status
- `sendChatMessage()` - Send chat messages to the API
- `clearConversation()` - Clear conversation history
- `getTokenCount()` - Get current token usage

#### chat.js (ChatManager)
- Manages chat UI interactions
- Handles message display and streaming
- Controls input state (enable/disable)
- Manages error display

#### prompt.js (PromptManager)
- Toggles prompt display on/off
- Displays full prompts sent to the model
- Manages copy-to-clipboard functionality

#### status.js (StatusManager)
- Updates connection status indicator
- Shows connection state (connected/warning/disconnected)
- Updates token limit display

#### tokens.js (TokenManager)
- Updates token counter display
- Manages progress bar visualization
- Changes colors based on usage levels

### Utilities

#### dom.js
- `escapeHtml()` - Safely escape HTML content
- `scrollToBottom()` - Scroll element to bottom
- `createElement()` - Create DOM elements with classes

#### storage.js
- Session ID management
- Show/hide prompts preference
- Local storage wrapper functions

## ES6 Modules

The code uses ES6 modules for clean imports/exports:
- All modules export classes or functions
- The main app.js imports what it needs
- Dependencies are clear and explicit
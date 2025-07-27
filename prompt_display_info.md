# Prompt Display Feature

A new feature has been added to display the full prompt sent to the model, which helps with debugging and understanding the conversation context.

## How to Use

1. **Start the app**: 
   ```bash
   source venv/bin/activate && python run.py
   ```

2. **Toggle Prompt Display**:
   - Click the purple "Show Prompt" button
   - The button will change to "Hide Prompt"
   - Your preference is saved in browser storage

3. **View Prompts**:
   - When enabled, each message will show the full prompt sent to the model
   - The prompt appears in a gray box between your message and the response
   - Shows the complete conversation history included in the context

4. **Copy Prompts**:
   - Each prompt display has a "Copy" button
   - Click to copy the full prompt to clipboard

## What You'll See

The prompt includes:
- All previous conversation exchanges (up to 10)
- Formatted as "Human: [your message]" followed by the assistant's response
- The current message at the end

Example prompt:
```
Human: Hello

Hi there! How can I help you today?
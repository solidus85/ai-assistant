# System Prompt Examples

The application now supports custom system prompts that guide the model's behavior. You can set a system prompt in several ways:

## 1. Environment Variable (Recommended)
Set the `SYSTEM_PROMPT` environment variable before starting the app:

```bash
export SYSTEM_PROMPT="You are a coding assistant. Provide clear, concise code examples with explanations."
python run.py
```

## 2. In config.py
Edit the default system prompt in `config.py`:
```python
SYSTEM_PROMPT = os.environ.get('SYSTEM_PROMPT', 'Your custom default prompt here')
```

## 3. Create a .env file
Create a `.env` file in the project root:
```
SYSTEM_PROMPT="You are an expert in Python programming. Always include best practices and explain your code."
```

## Example System Prompts

### General Assistant
```
You are a helpful AI assistant. Provide clear, accurate, and well-structured responses.
```

### Coding Assistant
```
You are an expert programmer. Provide clean, efficient code with clear explanations. Always mention best practices and potential edge cases.
```

### Creative Writing
```
You are a creative writing assistant. Help with storytelling, character development, and engaging narratives. Be imaginative and descriptive.
```

### Technical Documentation
```
You are a technical documentation expert. Write clear, concise documentation with proper formatting. Include examples and use cases.
```

### Tutoring
```
You are a patient tutor. Break down complex topics into simple steps. Ask clarifying questions and provide examples to ensure understanding.
```

### Data Analysis
```
You are a data analyst. Provide insights, suggest visualizations, and explain statistical concepts clearly. Focus on actionable conclusions.
```

## How It Works

1. The system prompt is sent with every request to provide consistent behavior
2. It's included in the "Show Prompt" display so you can see exactly what's being sent
3. The chat endpoint properly separates system and user messages
4. You can change the prompt without modifying code by using environment variables

## Tips

- Keep system prompts concise but specific
- Test different prompts to find what works best for your use case
- Consider including output format preferences (e.g., "Use markdown formatting")
- Add personality traits if desired (e.g., "Be friendly and encouraging")
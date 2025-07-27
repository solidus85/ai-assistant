# Context Window Size Impact on Speed

## Quick Reference

| Context Size | Speed Impact | Best For |
|-------------|--------------|----------|
| 4K (4,096) | Fastest ⚡⚡⚡ | Quick queries, single questions |
| **8K (8,192)** | Fast ⚡⚡ | **Most conversations (current)** |
| 16K (16,384) | Moderate ⚡ | Long conversations, code review |
| 32K (32,768) | Slower 🐌 | Very long documents |

## Speed Improvements by Context Size

### For Llama 3.1 8B:
- **32K → 16K**: ~25% faster
- **16K → 8K**: ~20-30% faster ✅ (your current change)
- **8K → 4K**: ~15-20% faster

### Expected Response Times with 8K Context:
- **Llama 3.1**: ~2 seconds (was 2-3s with 16K)
- **Mistral**: ~1-1.5 seconds
- **Mixtral**: ~15-20 seconds (was 25-30s)

## Trade-offs

### 8K Context (Current Setting):
**Pros:**
- ✅ 20-30% faster responses
- ✅ Still enough for most conversations
- ✅ Good for coding questions
- ✅ Handles ~10-15 messages of history

**Cons:**
- ❌ May truncate very long code files
- ❌ Less conversation history
- ❌ Might lose context in long chats

### When to Use Different Sizes:

**4K Context** - Use when:
- You need maximum speed
- Single question/answer
- No conversation history needed
```bash
python utilities/speed_profiles.py fast
```

**8K Context** - Use when:
- Daily conversations
- Moderate code snippets
- Balance of speed/context
```bash
python utilities/speed_profiles.py balanced
```

**16K Context** - Use when:
- Reviewing longer code
- Need more conversation history
- Complex multi-turn discussions
```bash
python utilities/speed_profiles.py quality
```

## Quick Commands

```bash
# Check current context size
echo $NUM_CTX

# Set context size temporarily
export NUM_CTX=8192

# Use speed profiles for easy switching
python utilities/speed_profiles.py balanced
```

Your current 8K setting provides a great balance - you'll notice faster responses while still having enough context for most tasks!
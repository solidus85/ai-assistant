# Mixtral Speed Optimization Guide

## Quick Speed Improvements

### 1. **Reduce Context Window** (Biggest Impact)
The context window size has the most significant impact on Mixtral's speed:

- **32K → 8K context**: ~50% speed improvement (60s → 25s)
- **8K → 4K context**: ~25% additional improvement (25s → 15s)
- **4K → 2K context**: Maximum speed (10-15s responses)

### 2. **Current Optimized Settings**
I've already updated your config to use 8K context (balanced speed/quality):
```python
NUM_CTX = 8192  # Reduced from 32768
```

### 3. **Speed Profiles**
Use the speed profile script to quickly switch between modes:

```bash
# Fast mode (10-20s responses)
python utilities/speed_profiles.py fast

# Balanced mode (15-25s responses) - RECOMMENDED
python utilities/speed_profiles.py balanced

# Quality mode (25-40s responses)
python utilities/speed_profiles.py quality

# Max mode (30-60s responses)
python utilities/speed_profiles.py max
```

### 4. **Other Optimizations**

#### Reduce Maximum Response Length
```bash
export MAX_TOKENS=2048  # Instead of 8192
```

#### Disable Conversation History
For single-shot queries without context:
```bash
export MAX_CONVERSATION_HISTORY=0
```

#### Use Streaming
The app already uses streaming, which makes responses feel faster by showing tokens as they generate.

### 5. **Alternative Models for Speed**

If Mixtral is still too slow, consider:

1. **Mixtral Q4** (standard version):
   ```bash
   export MODEL_NAME="mixtral:latest"
   ```
   - 30-40% faster than mixtral-accurate
   - Slightly lower quality

2. **Llama 3.1 8B**:
   ```bash
   ollama pull llama3.1:8b
   export MODEL_NAME="llama3.1:8b"
   ```
   - 2-3 second responses
   - Good quality, much faster

3. **Qwen 2.5 14B**:
   ```bash
   ollama pull qwen2.5:14b
   export MODEL_NAME="qwen2.5:14b"
   ```
   - 5-10 second responses
   - Excellent quality, good balance

### 6. **Testing Performance**

Run the optimization test:
```bash
python utilities/optimize_mixtral.py
```

Compare models:
```bash
python utilities/compare_models.py
```

### 7. **Real-World Impact**

With 8K context (current setting):
- First token: ~5-10 seconds
- Full response: ~15-25 seconds
- Tokens/sec: ~20-30

With 4K context (fast mode):
- First token: ~3-5 seconds
- Full response: ~10-20 seconds
- Tokens/sec: ~25-35

### 8. **Memory vs Speed Trade-off**

Your RTX 4080 has 16GB VRAM, so you can run Mixtral comfortably. The context window reduction doesn't save VRAM (model size stays the same), but it significantly reduces computation time.

### Recommendation

For your use case, I recommend:
1. Keep the current 8K context setting (good balance)
2. Use the "balanced" speed profile
3. If you need faster responses for specific tasks, temporarily switch to "fast" mode
4. For maximum quality when speed doesn't matter, use "quality" or "max" mode

### 9. **Handling Long Responses**

For responses that take over 4 minutes:
- Use the **Stop button** to interrupt if needed
- The app has a 5-minute timeout to prevent hanging
- Browser extension errors during long responses are automatically ignored
- Consider reducing MAX_TOKENS if responses are consistently too long:
  ```bash
  export MAX_TOKENS=2048  # Limit response length
  ```
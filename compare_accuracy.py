#!/usr/bin/env python3
"""
Compare accuracy between different quantization levels
"""

test_prompts = [
    "Explain the mathematical proof of Fermat's Last Theorem",
    "Write a Python function to implement binary search",
    "What is the exact value of pi to 15 decimal places?",
    "Translate 'Hello world' to Japanese, Chinese, and Arabic",
    "Calculate 1729 * 4096 / 137",
]

print("Accuracy Comparison Test")
print("=" * 50)
print("\nRun this after setting up models to compare outputs")
print("\nTest prompts:")
for i, prompt in enumerate(test_prompts, 1):
    print(f"{i}. {prompt}")
print("\nModels will show differences in:")
print("- Mathematical precision")
print("- Code accuracy")
print("- Language understanding")
print("- Factual recall")

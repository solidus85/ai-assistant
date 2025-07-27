#!/usr/bin/env python3
"""Compare model quality and capabilities."""

print("Model Quality Comparison")
print("=" * 70)
print()

models = {
    "Mistral 7B": {
        "speed": "1-2 seconds ⚡",
        "quality": "★★★☆☆ (Good)",
        "strengths": [
            "Extremely fast responses",
            "Good for simple Q&A",
            "Basic coding tasks",
            "Low resource usage"
        ],
        "weaknesses": [
            "Less nuanced reasoning",
            "Simpler code generation",
            "May miss context subtleties"
        ],
        "best_for": "Quick queries, simple tasks, chat"
    },
    
    "Llama 3.1 8B": {
        "speed": "2-3 seconds (was 7-8s, optimized)",
        "quality": "★★★★☆ (Very Good)",
        "strengths": [
            "Latest Meta AI technology",
            "Excellent reasoning",
            "Strong code understanding",
            "Good at following instructions",
            "Better context awareness"
        ],
        "weaknesses": [
            "Slightly slower than Mistral",
            "Uses more VRAM (~5GB)"
        ],
        "best_for": "Daily use, coding, complex queries"
    },
    
    "Phi3 Mini": {
        "speed": "1-2 seconds",
        "quality": "★★☆☆☆ (Basic)",
        "strengths": [
            "Very fast",
            "Minimal resource usage",
            "Good for simple tasks"
        ],
        "weaknesses": [
            "Limited reasoning",
            "Basic responses only",
            "May hallucinate more"
        ],
        "best_for": "Very simple queries, testing"
    },
    
    "Mixtral 8x7B": {
        "speed": "20-60 seconds",
        "quality": "★★★★★ (Excellent)",
        "strengths": [
            "Best quality available",
            "Expert-level reasoning",
            "Excellent for complex code",
            "Most accurate responses"
        ],
        "weaknesses": [
            "Very slow",
            "High VRAM usage (15-16GB)",
            "Overkill for simple tasks"
        ],
        "best_for": "Complex problems, accuracy critical"
    }
}

for model, info in models.items():
    print(f"\n{model}")
    print("-" * len(model))
    print(f"Speed: {info['speed']}")
    print(f"Quality: {info['quality']}")
    print(f"\nStrengths:")
    for s in info['strengths']:
        print(f"  • {s}")
    print(f"\nWeaknesses:")
    for w in info['weaknesses']:
        print(f"  • {w}")
    print(f"\nBest for: {info['best_for']}")

print("\n" + "=" * 70)
print("\n🎯 RECOMMENDATION: Llama 3.1 8B offers the best balance!")
print("   - Much better quality than Mistral")
print("   - Still fast enough for interactive use")
print("   - Latest model with strong capabilities")
print("\n💡 TIP: Use 'python utilities/switch_model.py' to change models anytime")
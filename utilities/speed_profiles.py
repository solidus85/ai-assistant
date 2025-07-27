#!/usr/bin/env python3
"""Switch between different speed profiles for Mixtral."""
import os
import sys

SPEED_PROFILES = {
    'fast': {
        'NUM_CTX': '4096',
        'MAX_TOKENS': '2048',
        'description': 'Fast mode: 4K context, ~10-20s responses'
    },
    'balanced': {
        'NUM_CTX': '8192',
        'MAX_TOKENS': '4096',
        'description': 'Balanced mode: 8K context, ~15-25s responses'
    },
    'quality': {
        'NUM_CTX': '16384',
        'MAX_TOKENS': '8192',
        'description': 'Quality mode: 16K context, ~25-40s responses'
    },
    'max': {
        'NUM_CTX': '32768',
        'MAX_TOKENS': '8192',
        'description': 'Max mode: 32K context, ~30-60s responses'
    }
}

def set_profile(profile_name):
    """Set environment variables for a specific profile."""
    if profile_name not in SPEED_PROFILES:
        print(f"Error: Unknown profile '{profile_name}'")
        print(f"Available profiles: {', '.join(SPEED_PROFILES.keys())}")
        return False
    
    profile = SPEED_PROFILES[profile_name]
    print(f"\nSetting speed profile: {profile_name}")
    print(f"Description: {profile['description']}")
    
    # Create or update .env file
    env_content = []
    env_vars = {
        'NUM_CTX': profile['NUM_CTX'],
        'MAX_TOKENS': profile['MAX_TOKENS']
    }
    
    # Read existing .env if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if not any(line.startswith(f"{key}=") for key in env_vars):
                    env_content.append(line.rstrip())
    
    # Add new values
    for key, value in env_vars.items():
        env_content.append(f"{key}={value}")
        print(f"  {key}={value}")
    
    # Write back
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content) + '\n')
    
    print(f"\nProfile '{profile_name}' has been set!")
    print("Restart your Flask app to apply changes.")
    return True

def show_profiles():
    """Show all available profiles."""
    print("Available Speed Profiles for Mixtral:")
    print("=" * 60)
    for name, profile in SPEED_PROFILES.items():
        print(f"\n{name.upper()}:")
        print(f"  {profile['description']}")
        print(f"  NUM_CTX: {profile['NUM_CTX']}")
        print(f"  MAX_TOKENS: {profile['MAX_TOKENS']}")

def main():
    if len(sys.argv) < 2:
        show_profiles()
        print("\nUsage: python speed_profiles.py <profile_name>")
        print("Example: python speed_profiles.py fast")
        return
    
    profile_name = sys.argv[1].lower()
    set_profile(profile_name)

if __name__ == "__main__":
    main()
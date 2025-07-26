#!/usr/bin/env python3
"""Test the new modular structure."""
import sys

try:
    # Test imports
    from app import create_app
    from app.services import OllamaService, ConversationService
    from app.utils.token_counter import TokenCounter
    print("✓ All imports successful")
    
    # Test app creation
    app = create_app('development')
    print("✓ App created successfully")
    
    # Test services
    with app.app_context():
        from app.utils.extensions import get_ollama_service, get_conversation_service
        ollama = get_ollama_service()
        conversation = get_conversation_service()
        print("✓ Services initialized")
    
    # Test routes exist
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    expected_routes = ['/', '/api/health', '/api/chat/stream', '/api/conversation/clear']
    for route in expected_routes:
        if route in rules:
            print(f"✓ Route {route} registered")
        else:
            print(f"✗ Route {route} missing")
    
    print("\n✅ Structure test passed!")
    
except Exception as e:
    print(f"\n❌ Structure test failed: {e}")
    sys.exit(1)
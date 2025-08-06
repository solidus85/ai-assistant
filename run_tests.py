#!/usr/bin/env python3
"""Simple test runner to verify tests work."""
import sys
import unittest
import os

# Add project to path
sys.path.insert(0, os.path.abspath('.'))

# Import all test modules
from tests.unit.services import test_ollama_service, test_conversation_service
from tests.unit.api import test_health, test_chat, test_conversation, test_settings
from tests.unit.utils import test_token_counter
from tests import test_app

def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test modules
    test_modules = [
        test_ollama_service,
        test_conversation_service,
        test_health,
        test_chat,
        test_conversation,
        test_settings,
        test_token_counter,
        test_app
    ]
    
    for module in test_modules:
        suite.addTests(loader.loadTestsFromModule(module))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
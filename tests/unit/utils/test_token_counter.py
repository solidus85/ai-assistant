"""Unit tests for TokenCounter utility."""
import pytest
from src.utils.token_counter import TokenCounter


class TestTokenCounter:
    """Test cases for TokenCounter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.counter = TokenCounter()
    
    def test_count_empty_text(self):
        """Test counting tokens in empty text."""
        assert self.counter.count("") == 0
        assert self.counter.count(None) == 0
    
    def test_count_simple_text(self):
        """Test counting tokens in simple text."""
        text = "Hello world"
        count = self.counter.count(text)
        # Should be approximately 2-3 tokens
        assert 1 <= count <= 4
    
    def test_count_longer_text(self):
        """Test counting tokens in longer text."""
        text = "The quick brown fox jumps over the lazy dog. " * 10
        count = self.counter.count(text)
        # Approximately 90-130 tokens for this text
        assert 70 <= count <= 150
    
    def test_count_with_punctuation(self):
        """Test that punctuation affects token count."""
        text1 = "Hello world"
        text2 = "Hello, world! How are you?"
        
        count1 = self.counter.count(text1)
        count2 = self.counter.count(text2)
        
        assert count2 > count1
    
    def test_count_with_whitespace(self):
        """Test that whitespace affects token count."""
        text1 = "Helloworld"
        text2 = "Hello world"
        text3 = "Hello\nworld\ttab"
        
        count1 = self.counter.count(text1)
        count2 = self.counter.count(text2)
        count3 = self.counter.count(text3)
        
        assert count2 >= count1
        assert count3 >= count1
    
    def test_count_special_characters(self):
        """Test counting with special characters."""
        text = "Email: test@example.com, URL: https://example.com"
        count = self.counter.count(text)
        
        # Should handle special characters reasonably
        assert count > 0
        assert count < len(text)  # Should be less than character count
    
    def test_count_unicode_text(self):
        """Test counting with Unicode characters."""
        text = "Hello 世界 🌍 مرحبا"
        count = self.counter.count(text)
        
        assert count > 0
        # Unicode might count differently but should still work
    
    def test_minimum_token_count(self):
        """Test that non-empty text always has at least 1 token."""
        assert self.counter.count("a") >= 1
        assert self.counter.count(".") >= 1
        assert self.counter.count(" ") >= 1
    
    def test_model_parameter(self):
        """Test initialization with different model names."""
        counter1 = TokenCounter(model="gemma")
        counter2 = TokenCounter(model="llama2")
        
        # Both should work the same way for our estimation
        text = "Test message"
        assert counter1.count(text) == counter2.count(text)
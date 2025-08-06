"""Unit tests for keyword extractor service."""
import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime
from src.services.keyword_extractor import KeywordExtractor


class TestKeywordExtractor:
    """Test keyword extraction service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_ollama = Mock()
        self.extractor = KeywordExtractor(self.mock_ollama, 'phi3')
    
    def test_extract_email_info_success(self):
        """Test successful email information extraction."""
        # Mock Ollama response
        self.mock_ollama.generate.return_value = {
            'response': json.dumps({
                'project_name': 'Test Project',
                'company': 'Test Corp',
                'people': ['John Doe', 'Jane Smith'],
                'keywords': ['meeting', 'deadline', 'review'],
                'action_items': ['Review document', 'Schedule meeting'],
                'deliverables': ['Final report by Friday'],
                'importance': 'high',
                'summary': 'Meeting scheduled to review project deadline'
            })
        }
        
        result = self.extractor.extract_email_info(
            'Email content about meeting and deadline',
            'Project Update'
        )
        
        assert result['project_name'] == 'Test Project'
        assert result['company'] == 'Test Corp'
        assert len(result['people']) == 2
        assert 'meeting' in result['keywords']
        assert result['importance'] == 'high'
    
    def test_extract_email_info_with_invalid_json(self):
        """Test email extraction with invalid JSON response."""
        # Mock Ollama with invalid JSON
        self.mock_ollama.generate.return_value = {
            'response': 'Not valid JSON {incomplete'
        }
        
        result = self.extractor.extract_email_info(
            'Email content',
            'Subject'
        )
        
        # Should return fallback extraction
        assert result['project_name'] is None
        assert result['importance'] == 'medium'
        assert len(result['keywords']) > 0  # Simple extraction should work
    
    def test_extract_email_info_exception_handling(self):
        """Test email extraction when Ollama fails."""
        # Mock Ollama to raise exception
        self.mock_ollama.generate.side_effect = Exception('API Error')
        
        result = self.extractor.extract_email_info(
            'Email content with some keywords',
            'Test Subject'
        )
        
        # Should return fallback extraction
        assert result['project_name'] is None
        assert 'Email content' in result['summary'] or 'Test Subject' in result['summary']
        assert len(result['keywords']) > 0
    
    def test_extract_status_update_info_success(self):
        """Test successful status update extraction."""
        self.mock_ollama.generate.return_value = {
            'response': json.dumps({
                'update_type': 'progress',
                'keywords': ['development', 'testing', 'complete'],
                'percentage_complete': 75,
                'blockers': ['API integration issue'],
                'next_steps': ['Code review', 'Deploy to staging'],
                'deliverables_mentioned': ['API documentation'],
                'people_mentioned': ['Bob Johnson']
            })
        }
        
        result = self.extractor.extract_status_update_info(
            'Development is 75% complete. API integration issue blocking progress.',
            'Project Alpha'
        )
        
        assert result['update_type'] == 'progress'
        assert result['percentage_complete'] == 75
        assert len(result['blockers']) == 1
        assert 'development' in result['keywords']
    
    def test_extract_status_update_info_fallback(self):
        """Test status update extraction fallback."""
        self.mock_ollama.generate.side_effect = Exception('Failed')
        
        result = self.extractor.extract_status_update_info(
            'Status update content',
            'Project'
        )
        
        assert result['update_type'] == 'general'
        assert result['percentage_complete'] is None
        assert len(result['keywords']) > 0
    
    def test_extract_dates(self):
        """Test date extraction from text."""
        text = """
        The deadline is 2024-12-25.
        Meeting scheduled for tomorrow.
        Report due on Jan 15, 2025.
        Review by end of month.
        """
        
        dates = self.extractor.extract_dates(text)
        
        assert len(dates) >= 3
        assert any('2024-12-25' in d['original_text'] for d in dates)
        assert any('tomorrow' in d['original_text'].lower() for d in dates)
        assert any('Jan 15' in d['original_text'] for d in dates)
    
    def test_clean_people_list(self):
        """Test cleaning people names."""
        people = [
            'John Doe',
            'jane@email.com',  # Should be removed (email)
            'Bob',
            '  Alice Smith  ',  # Should be trimmed
            'J',  # Should be removed (too short)
            'Bob'  # Duplicate
        ]
        
        cleaned = self.extractor._clean_people_list(people)
        
        assert 'John Doe' in cleaned
        assert 'Alice Smith' in cleaned
        assert 'Bob' in cleaned
        assert 'jane@email.com' not in cleaned
        assert 'J' not in cleaned
        assert len(cleaned) == 3  # No duplicates
    
    def test_clean_people_list_invalid_input(self):
        """Test cleaning with invalid input."""
        assert self.extractor._clean_people_list(None) == []
        assert self.extractor._clean_people_list('not a list') == []
        assert self.extractor._clean_people_list([123, None]) == []
    
    def test_clean_keywords(self):
        """Test keyword cleaning."""
        keywords = [
            'Important',
            'AI',  # Too short, should be removed
            '  machine learning  ',
            'Important',  # Duplicate
            ''  # Empty
        ]
        
        cleaned = self.extractor._clean_keywords(keywords)
        
        assert 'important' in cleaned  # Lowercased
        assert 'machine learning' in cleaned
        assert len(cleaned) == 2  # No duplicates, no short words
    
    def test_clean_keywords_invalid_input(self):
        """Test keyword cleaning with invalid input."""
        result = self.extractor._clean_keywords('not a list')
        assert isinstance(result, list)
        assert len(result) > 0  # Should extract simple keywords
    
    def test_parse_deliverables(self):
        """Test deliverable parsing."""
        deliverables = [
            {'title': 'Task 1', 'due_date': '2024-12-25'},
            'Complete documentation by Friday',
            'Review code'
        ]
        
        parsed = self.extractor._parse_deliverables(deliverables)
        
        assert len(parsed) == 3
        assert parsed[0]['title'] == 'Task 1'
        assert parsed[1]['title'] == 'Complete documentation by Friday'
        # May have extracted date for second item
    
    def test_parse_deliverables_empty(self):
        """Test parsing empty deliverables."""
        assert self.extractor._parse_deliverables(None) == []
        assert self.extractor._parse_deliverables([]) == []
        assert self.extractor._parse_deliverables('') == []
    
    def test_extract_simple_keywords(self):
        """Test simple keyword extraction without LLM."""
        text = """
        This is a test document about machine learning and artificial intelligence.
        The project involves data analysis and model training.
        Machine learning is important for this project.
        """
        
        keywords = self.extractor._extract_simple_keywords(text)
        
        assert 'machine' in keywords  # Should be top keyword (appears twice)
        assert 'learning' in keywords
        assert 'project' in keywords
        assert len(keywords) <= 10
        # Stop words should be filtered
        assert 'the' not in keywords
        assert 'is' not in keywords
    
    def test_parse_relative_date_today(self):
        """Test parsing 'today' and similar."""
        today_date = self.extractor._parse_relative_date('today')
        assert today_date is not None
        assert today_date.hour == 17  # EOD
        
        eod_date = self.extractor._parse_relative_date('eod')
        assert eod_date is not None
        assert eod_date.hour == 17
    
    def test_parse_relative_date_tomorrow(self):
        """Test parsing 'tomorrow'."""
        tomorrow = self.extractor._parse_relative_date('tomorrow')
        assert tomorrow is not None
        
        from datetime import datetime, timedelta
        now = datetime.now()
        expected = (now + timedelta(days=1)).date()
        assert tomorrow.date() == expected
    
    def test_parse_relative_date_next_week(self):
        """Test parsing 'next week'."""
        next_week = self.extractor._parse_relative_date('next week')
        assert next_week is not None
        
        from datetime import datetime, timedelta
        now = datetime.now()
        assert next_week > now
        assert next_week <= now + timedelta(weeks=1, days=1)
    
    def test_parse_relative_date_invalid(self):
        """Test parsing invalid relative dates."""
        assert self.extractor._parse_relative_date('invalid') is None
        assert self.extractor._parse_relative_date('') is None
    
    def test_fallback_extraction(self):
        """Test fallback extraction method."""
        content = "This is test content with important keywords and information"
        subject = "Test Subject"
        
        result = self.extractor._fallback_extraction(content, subject)
        
        assert result['project_name'] is None
        assert result['company'] is None
        assert result['people'] == []
        assert len(result['keywords']) > 0
        assert 'important' in result['keywords']
        assert result['importance'] == 'medium'
        # Summary could be from content or subject
        assert 'test' in result['summary'].lower() or 'content' in result['summary'].lower()
    
    def test_fallback_extraction_long_content(self):
        """Test fallback with long content."""
        content = "x" * 200
        result = self.extractor._fallback_extraction(content, None)
        
        assert len(result['summary']) < len(content)
        assert '...' in result['summary']
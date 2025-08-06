"""Keyword extraction service using Ollama with smaller models."""
import json
import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extract keywords and entities from text using LLM."""
    
    def __init__(self, ollama_service, model_name: str = "phi3"):
        self.ollama = ollama_service
        self.model_name = model_name
        
    def extract_email_info(self, email_content: str, subject: str = None) -> Dict[str, Any]:
        """Extract structured information from email content."""
        prompt = f"""Extract the following information from this email:
        
Subject: {subject or 'N/A'}
Content: {email_content}

Please identify and return in JSON format:
1. project_name: The project or initiative being discussed
2. company: The company or organization mentioned
3. people: List of people's names mentioned (not email addresses)
4. keywords: Important keywords and topics (5-10 words)
5. action_items: Any action items or tasks mentioned
6. deliverables: Any deliverables mentioned with due dates if available
7. importance: Rate as 'high', 'medium', or 'low' based on content urgency
8. summary: A brief 1-2 sentence summary

Return ONLY valid JSON, no other text."""

        try:
            response = self.ollama.generate(prompt, options={
                "temperature": 0.3,
                "num_predict": 500
            })
            
            response_text = response.get('response', '{}')
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            extracted = json.loads(response_text)
            
            extracted['people'] = self._clean_people_list(extracted.get('people', []))
            extracted['keywords'] = self._clean_keywords(extracted.get('keywords', []))
            extracted['deliverables'] = self._parse_deliverables(extracted.get('deliverables', []))
            
            return extracted
            
        except Exception as e:
            logger.error(f"Failed to extract email info: {e}")
            return self._fallback_extraction(email_content, subject)
    
    def extract_status_update_info(self, status_content: str, project_name: str = None) -> Dict[str, Any]:
        """Extract structured information from status update."""
        prompt = f"""Extract information from this project status update:
        
Project: {project_name or 'Unknown'}
Status Update: {status_content}

Please identify and return in JSON format:
1. update_type: Type of update ('progress', 'blocker', 'completion', 'risk', 'general')
2. keywords: Key topics and terms (5-10 words)
3. percentage_complete: If mentioned, the completion percentage (number only)
4. blockers: List any blockers or issues
5. next_steps: List of next steps or upcoming tasks
6. deliverables_mentioned: Any deliverables referenced
7. people_mentioned: Names of people mentioned

Return ONLY valid JSON, no other text."""

        try:
            response = self.ollama.generate(prompt, options={
                "temperature": 0.3,
                "num_predict": 400
            })
            
            response_text = response.get('response', '{}')
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            extracted = json.loads(response_text)
            
            extracted['keywords'] = self._clean_keywords(extracted.get('keywords', []))
            
            return extracted
            
        except Exception as e:
            logger.error(f"Failed to extract status update info: {e}")
            return {
                'update_type': 'general',
                'keywords': self._extract_simple_keywords(status_content),
                'percentage_complete': None,
                'blockers': [],
                'next_steps': [],
                'deliverables_mentioned': [],
                'people_mentioned': []
            }
    
    def extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract dates and deadlines from text."""
        dates = []
        
        date_patterns = [
            r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b',
            r'\b(\d{4}-\d{2}-\d{2})\b',
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            r'\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
            r'\b(tomorrow|today|next week|next month|end of month|EOD|COB)\b'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    date_str = match.group()
                    
                    if date_str.lower() in ['tomorrow', 'today', 'eod', 'cob']:
                        parsed_date = self._parse_relative_date(date_str)
                    else:
                        parsed_date = date_parser.parse(date_str, fuzzy=True)
                    
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(text), match.end() + 50)
                    context = text[context_start:context_end]
                    
                    dates.append({
                        'date': parsed_date.isoformat() if parsed_date else None,
                        'original_text': date_str,
                        'context': context
                    })
                except:
                    continue
        
        return dates
    
    def _clean_people_list(self, people: List) -> List[str]:
        """Clean and normalize people names."""
        if not isinstance(people, list):
            return []
        
        cleaned = []
        for person in people:
            if isinstance(person, str):
                name = person.strip()
                if '@' not in name and len(name) > 2:
                    cleaned.append(name)
        
        return list(set(cleaned))
    
    def _clean_keywords(self, keywords: List) -> List[str]:
        """Clean and normalize keywords."""
        if not isinstance(keywords, list):
            return self._extract_simple_keywords(str(keywords))
        
        cleaned = []
        for keyword in keywords:
            if isinstance(keyword, str):
                kw = keyword.strip().lower()
                if len(kw) > 2:
                    cleaned.append(kw)
        
        return list(set(cleaned))
    
    def _parse_deliverables(self, deliverables: Any) -> List[Dict[str, Any]]:
        """Parse deliverables into structured format."""
        if not deliverables:
            return []
        
        if isinstance(deliverables, str):
            deliverables = [deliverables]
        
        parsed = []
        for item in deliverables:
            if isinstance(item, dict):
                parsed.append(item)
            elif isinstance(item, str):
                dates = self.extract_dates(item)
                parsed.append({
                    'title': item,
                    'due_date': dates[0]['date'] if dates else None
                })
        
        return parsed
    
    def _extract_simple_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction without LLM."""
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 
                     'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that',
                     'this', 'it', 'from', 'be', 'are', 'was', 'were', 'been'}
        
        words = re.findall(r'\b[a-z]+\b', text.lower())
        keywords = []
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                keywords.append(word)
        
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in sorted_words[:10]]
    
    def _parse_relative_date(self, date_str: str) -> Optional[datetime]:
        """Parse relative date strings."""
        from datetime import timedelta
        
        date_str = date_str.lower()
        now = datetime.now()
        
        if date_str == 'today' or date_str in ['eod', 'cob']:
            return now.replace(hour=17, minute=0, second=0, microsecond=0)
        elif date_str == 'tomorrow':
            return (now + timedelta(days=1)).replace(hour=17, minute=0, second=0, microsecond=0)
        elif date_str == 'next week':
            return now + timedelta(weeks=1)
        elif date_str == 'next month':
            return now + timedelta(days=30)
        elif date_str == 'end of month':
            next_month = now.replace(day=28) + timedelta(days=4)
            return (next_month - timedelta(days=next_month.day)).replace(
                hour=17, minute=0, second=0, microsecond=0
            )
        
        return None
    
    def _fallback_extraction(self, content: str, subject: str = None) -> Dict[str, Any]:
        """Fallback extraction when LLM fails."""
        return {
            'project_name': None,
            'company': None,
            'people': [],
            'keywords': self._extract_simple_keywords(content),
            'action_items': [],
            'deliverables': [],
            'importance': 'medium',
            'summary': (subject or content[:100]) + '...' if len(content) > 100 else content
        }
"""Service for interacting with Ollama API."""
import requests
import json
import logging
from typing import Generator, Dict, Any, Optional

logger = logging.getLogger(__name__)


class OllamaService:
    """Handles all Ollama API interactions."""
    
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
        
    def check_health(self) -> Dict[str, Any]:
        """Check if Ollama service is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                return {
                    'status': 'connected',
                    'model_available': self.model_name in model_names,
                    'models': model_names
                }
            else:
                return {'status': 'error', 'message': 'Failed to connect'}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {'status': 'disconnected', 'message': str(e)}
    
    def generate_stream(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]:
        """Generate streaming response from Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": options or {}
        }
        
        try:
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        yield chunk
                        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            yield {"error": str(e), "done": True}
    
    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate non-streaming response from Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": options or {}
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            return {"error": str(e)}
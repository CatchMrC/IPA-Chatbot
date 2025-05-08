from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
import json
import logging
from ..config.config import settings

class LLMAdapter(ABC):
    """Basisklasse fuer LLM-Adapter"""
    
    @abstractmethod
    async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """Generiere eine Antwort vom LLM"""
        pass

class OllamaAdapter(LLMAdapter):
    """Adapter fuer die Ollama-API"""
    
    def __init__(self, api_url: str, model: str):
        self.api_url = api_url  # URL der Ollama-API
        self.model = model  # Verwendetes Modell
        
    async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """Generiere eine Antwort mit der Ollama-API"""
        try:
            # Erstelle die Nutzlast fuer die Anfrage
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,  # Temperatur fuer die Generierung
                    "top_p": 0.9  # Wahrscheinlichkeitsgrenze
                }
            }
            
            if max_tokens:
                payload["options"]["num_predict"] = max_tokens  # Maximale Tokenanzahl festlegen
                
            # Sende die Anfrage an die API
            response = requests.post(self.api_url, json=payload)
            
            if response.status_code == 200:
                # Erfolgreiche Antwort verarbeiten
                return {
                    "response": response.json()["response"].strip(),  # Generierte Antwort
                    "status": "success"  # Status der Anfrage
                }
            
            # Fehlerhafte Antwort verarbeiten
            return {
                "error": f"Anfrage fehlgeschlagen mit Status {response.status_code}",
                "status": "error"
            }
            
        except Exception as e:
            # Fehler protokollieren und zurueckgeben
            logging.error(f"Fehler im OllamaAdapter: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }
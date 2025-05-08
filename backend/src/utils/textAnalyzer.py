# Import der SentenceTransformer-Bibliothek zur Erstellung von Text-Embeddings
from sentence_transformers import SentenceTransformer
from typing import Dict, Any, List
import numpy as np

class TextAnalyzer:
    def __init__(self):
        # Initialisierung des Modells zur Erstellung von Text-Embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Erstellt ein Vektor-Embedding fuer den uebergebenen Text.
        
        :param text: Der Text, fuer den ein Embedding erstellt werden soll.
        :return: Eine Liste von Floats, die das Embedding darstellen.
        """
        return self.model.encode(text).tolist()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analysiert den uebergebenen Text und gibt verschiedene Merkmale zurueck.
        
        :param text: Der zu analysierende Text.
        :return: Ein Dictionary mit den Merkmalen:
                 - "embedding": Das Vektor-Embedding des Textes.
                 - "length": Die Laenge des Textes (Anzahl der Zeichen).
                 - "word_count": Die Anzahl der Woerter im Text.
        """
        return {
            "embedding": self.get_embedding(text),
            "length": len(text),  # Anzahl der Zeichen im Text
            "word_count": len(text.split())  # Anzahl der Woerter im Text
        }
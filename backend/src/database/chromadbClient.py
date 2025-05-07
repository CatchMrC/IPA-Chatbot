from src.config.config import settings  # Absolute Import verwenden
import chromadb
from typing import Dict, Any, Optional, List
from pathlib import Path

class ChromaDBClient:
    def __init__(self):
        # Initialisiert den ChromaDB-Client mit einem persistenten Speicherpfad
        self.client = chromadb.PersistentClient(path=str(settings.DB_PATH))
        
        # Erstellt oder holt eine Collection für Hardware-Produkte
        self.collection = self.client.get_or_create_collection(
            name="hardware_products"
        )
    
    def get_unique_values(self, field: str) -> set:
        """
        Gibt alle eindeutigen Werte für ein bestimmtes Feld zurück.
        
        :param field: Der Name des Feldes, für das die eindeutigen Werte abgerufen werden sollen.
        :return: Eine Menge von eindeutigen Werten (in Kleinbuchstaben).
        """
        results = self.collection.get()
        return {
            str(metadata.get(field, "")).lower() 
            for metadata in results["metadatas"] 
            if field in metadata and metadata[field]
        }

    def search_products(self, query_embedding: List[float], limit: int = 5):
        """
        Sucht Produkte basierend auf Vektorähnlichkeit.
        
        :param query_embedding: Der Vektor, der für die Suche verwendet wird.
        :param limit: Die maximale Anzahl der zurückzugebenden Ergebnisse.
        :return: Suchergebnisse aus der ChromaDB-Collection.
        """
        try:
            print("Abfrage der ChromaDB-Collection...")
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            print(f"{len(result.get('ids', [[]])[0])} Ergebnisse gefunden")
            return result
        except Exception as e:
            print(f"ChromaDB-Suchfehler: {e}")
            raise
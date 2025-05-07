from pathlib import Path
import sys
# Projektroot zum Python-Pfad hinzufügen
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
from src.database.chromadbClient import ChromaDBClient
# Daten-Überprüfung // Prüfen, ob die Daten korrekt importiert wurden


# Client initialisieren
db_client = ChromaDBClient()

# Einen bestimmten Datensatz abrufen
record_id = "1"  # Ersetzen Sie dies mit der ID, die Sie überprüfen möchten
result = db_client.collection.get(
    ids=[record_id],
    include=['metadatas', 'documents']
)

# Datensatzdetails ausgeben
print("Metadaten:", result['metadatas'][0])
print("\nDokument:", result['documents'][0])
import os
import sys
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Nur die erste GPU verwenden

# Projektroot zum Python-Pfad hinzufügen
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sentence_transformers import SentenceTransformer
from src.database.chromadbClient import ChromaDBClient
from src.config.config import settings

def clean_csv_value(value):
    """Bereinigt einzelne CSV-Werte"""
    if pd.isna(value):
        return ""
    cleaned = str(value).strip()
    cleaned = cleaned.replace('\n', ' ')  # Zeilenumbrüche entfernen
    cleaned = ' '.join(cleaned.split())  # Mehrfache Leerzeichen entfernen
    return cleaned

def clean_text(text):
    """Bereinigt und standardisiert Textwerte"""
    if pd.isna(text):
        return ""
    cleaned = clean_csv_value(text)
    special_chars = {
        '/': ' / ',  # Schrägstriche mit Leerzeichen umgeben
        '-': ' - ',  # Bindestriche mit Leerzeichen umgeben
        '_': ' ',    # Unterstriche durch Leerzeichen ersetzen
        '.': '. ',   # Punkte mit Leerzeichen danach versehen
        ',': ', '    # Kommas mit Leerzeichen danach versehen
    }
    for char, replacement in special_chars.items():
        cleaned = cleaned.replace(char, replacement)
    return ' '.join(cleaned.split())

def parse_tech_specs(tech_specs_str: str) -> dict:
    """Parst technische Spezifikationen aus einem String in ein strukturiertes Dictionary"""
    specs = {}
    if not tech_specs_str:
        return specs

    # Spezifikations-String in einzelne Komponenten aufteilen
    parts = [p.strip() for p in tech_specs_str.split(',')]
    
    for part in parts:
        if ':' in part:
            key, value = [p.strip() for p in part.split(':', 1)]
            specs[key.lower()] = value  # Schlüssel in Kleinbuchstaben umwandeln
    
    return specs

def tech_specs_to_string(specs: dict) -> str:
    """Konvertiert technische Spezifikationen aus einem Dictionary in einen formatierten String"""
    if not specs:
        return ""
    return ", ".join(f"{key}: {value}" for key, value in specs.items())

def create_searchable_text(row):
    """Erstellt durchsuchbaren Text, der alle relevanten Informationen enthält"""
    # Technische Spezifikationen parsen
    tech_specs = parse_tech_specs(row['tech_specs'])
    
    # Spezifikationstext dynamisch erstellen
    specs_text = "\n    ".join(
        f"{key}: {value}" 
        for key, value in tech_specs.items()
    )
    
    return f"""
    Benutzerprofil: {row['user_profile']}
    Ideal für: {row['ideal_for']}
    Nicht empfohlen für: {row['not_recommended_for']}
    Qualifikation: {row['qualification']}
    Typ: {row['type']}
    Produkt: {row['manufacturer']} {row['model']}
    Betriebssystem: {row['os']}
    Technische Spezifikationen:
    {specs_text}
    """.strip()

def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Liest eine CSV-Datei mit UTF-8-Kodierung ein"""
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            sep=',',
            quotechar='"',
            escapechar='\\',
            na_values=['', 'NA', 'N/A', '-'],
            dtype=str
        )
        print("CSV-Datei erfolgreich mit UTF-8-Kodierung geladen")
        return df
    except UnicodeDecodeError as e:
        print(f"Fehler: Datei ist nicht im UTF-8-Format. {e}")
        print("Bitte konvertieren Sie die Datei nach UTF-8 mit:")
        print(f"iconv -f ISO-8859-1 -t UTF-8 {file_path} > {file_path}.utf8")
        raise

def import_csv_to_chromadb():
    """Importiert Daten aus einer CSV-Datei in ChromaDB"""
    try:
        csv_path = settings.PRODUCT_DATA_PATH
        print(f"Lese CSV aus: {csv_path}")
        
        df = read_csv_file(csv_path)
        print(f"{len(df)} Datensätze erfolgreich aus CSV geladen")
        
        # Spalten, die in der CSV erwartet werden
        text_columns = [
            'user_profile', 'ideal_for', 'not_recommended_for',
            'qualification', 'type', 'manufacturer', 'model',
            'os', 'tech_specs', 'link'
        ]
        numeric_columns = ['price_chf']
        
        # Überprüfen, ob alle erforderlichen Spalten vorhanden sind
        missing_columns = [col for col in text_columns + numeric_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Fehlende erforderliche Spalten: {missing_columns}")
        
        # Textspalten bereinigen
        for col in text_columns:
            df[col] = df[col].apply(clean_text)

        # Embedding-Modell und Datenbank initialisieren
        model = SentenceTransformer('all-MiniLM-L6-v2')
        db_client = ChromaDBClient()
        
        # Bestehende Daten in der Datenbank löschen
        try:
            db_client.collection.delete(db_client.collection.get()["ids"])
            print("Bestehende Daten gelöscht")
        except Exception as e:
            print(f"Keine bestehenden Daten zum Löschen: {e}")

        # Daten für den Import vorbereiten
        embeddings = []
        documents = []
        metadatas = []
        ids = []

        total_rows = len(df)
        for idx, row in df.iterrows():
            try:
                if pd.isna(row['id']):
                    print(f"Überspringe Zeile {idx}: Fehlende ID")
                    continue

                search_text = create_searchable_text(row)
                product_name = f"{row['manufacturer']} {row['model']}"

                # Basis-Metadaten erstellen
                metadata = {
                    col: clean_text(str(row[col]))
                    for col in text_columns
                    if col != 'tech_specs' and pd.notna(row[col])
                }
                
                # Analysierte technische Spezifikationen zu Metadaten als String hinzufügen
                if pd.notna(row['tech_specs']):
                    parsed_specs = parse_tech_specs(row['tech_specs'])
                    metadata['tech_specs'] = tech_specs_to_string(parsed_specs)
                else:
                    metadata['tech_specs'] = ""

                # Numerische Felder hinzufügen
                if pd.notna(row['price_chf']):
                    try:
                        metadata['price_chf'] = float(str(row['price_chf']).replace('PCLCM', '0'))
                    except:
                        metadata['price_chf'] = 0

                embeddings.append(model.encode(search_text).tolist())
                documents.append(search_text)
                metadatas.append(metadata)
                ids.append(str(int(row['id'])))
                
                print(f"Verarbeite Datensatz {idx+1}/{total_rows}: {product_name}")

            except Exception as e:
                print(f"Fehler bei der Verarbeitung von Zeile {idx}: {e}")
                continue

        # Daten in ChromaDB importieren
        if embeddings:
            db_client.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print("\nImport-Zusammenfassung:")
            print(f"Gesamtanzahl Datensätze: {total_rows}")
            print(f"Erfolgreich importiert: {len(ids)}")
            print(f"Fehlgeschlagen/Übersprungen: {total_rows - len(ids)}")
        else:
            raise ValueError("Keine gültigen Datensätze zum Importieren")

    except Exception as e:
        print(f"Import-Fehler: {e}")
        raise

if __name__ == "__main__":
    import_csv_to_chromadb()
# IPA-Chatbot


it-hardware-chatbot/
├── backend/
│   ├── src/
│   │   ├── config/        # Application configuration
│   │   ├── database/      # ChromaDB integration
│   │   ├── models/        # Pydantic models
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Service providers
│   │   ├── utils/         # Utility functions
│   │   └── data/          # Data files & scripts
│   ├── main.py            # FastAPI application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   └── styles/        # CSS styles
│   ├── package.json       # npm dependencies
│   └── README.md          # Frontend documentation
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
└── README.md              # Project documentation


# IT Hardware Chatbot

Ein dynamischer Chatbot für IT-Hardware-Empfehlungen mit ChromaDB und Sentence Transformers.

---

## Projektinitialisieren

### Git Versionverwaltung

1. **Repository erstellen:**
   - Gehe zu [GitHub](https://github.com) und erstelle ein neues Repository.
   - Wähle einen passenden Namen für dein Projekt, z. B. `llm-hardware-chatbot`.

2. **Lokales Git-Repository initialisieren:**
   ```bash
   git init
   ```

3. **Remote-Repository hinzufügen:**
   ```bash
   git remote add origin https://github.com/CatchMrC/it-hardware-chatbot.git
   ```

4. **Erste Änderungen hinzufügen und commiten:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

### Backend Ordnerstruktur

Die empfohlene Struktur für den Backend-Ordner ist wie folgt:

```bash
backend/
├── src/
│   ├── config/        # Anwendungskonfiguration
│   ├── database/      # ChromaDB-Integration
│   ├── models/        # Pydantic-Modelle
│   ├── routes/        # API-Endpunkte
│   ├── services/      # Service-Anbieter
│   ├── utils/         # Hilfsfunktionen
│   └── data/          # Daten und Scripte
├── main.py            # FastAPI-Anwendungseinstiegspunkt
└── requirements.txt   # Python-Abhängigkeiten
```

Erstelle die Ordnerstruktur mit den folgenden Befehlen:

```bash
mkdir -p backend/src/{config,database,models,routes,services,utils,data}
touch backend/main.py backend/requirements.txt
```

### Virtuelle Python Umgebung (Miniconda3)

1. **Installiere Miniconda3:**
   - Lade Miniconda3 von [hier](https://docs.conda.io/en/latest/miniconda.html) herunter und installiere es.

2. **Erstelle eine neue virtuelle Umgebung:**
   ```bash
   conda create -n it-hardware-chatbot python=3.9
   ```

3. **Aktiviere die virtuelle Umgebung:**
   ```bash
   conda activate it-hardware-chatbot
   ```

4. **Installiere Abhängigkeiten:**
   - Füge `requirements.txt` die benötigten Python-Bibliotheken hinzu:
     ```
     fastapi
     uvicorn
     pydantic
     chromadb
     sentence-transformers
     ```
   - Installiere die Abhängigkeiten:
     ```bash
     pip install -r backend/requirements.txt
     ```

5. **Speichere die Umgebung:**
   - Exportiere die Umgebung in eine `environment.yml` Datei:
     ```bash
     conda env export > environment.yml
     ```

6. **Später die Umgebung wiederherstellen:**
   ```bash
   conda env create -f environment.yml
   ```

---



https://vectorpaint.yaks.co.nz/ für favicon - .svg erstellen
https://favicon.io/favicon-converter/ für favicon - .ico erstellen

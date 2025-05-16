# IPA-Chatbot

Ein intelligenter Chatbot für IT-Hardware-Empfehlungen mit Semantic Search und Natural Language Processing.

## Projektbeschreibung

Der IPA-Chatbot ist eine moderne Webanwendung, die Benutzern hilft, passende IT-Hardware-Produkte zu finden und Fragen zu IT-Themen zu beantworten. Das System nutzt ChromaDB für Vektorsuche und moderne NLP-Technologien, um präzise und kontextbezogene Antworten zu liefern.

## Features

- **Semantische Produktsuche**: Finde Produkte durch natürlichsprachige Anfragen
- **Kontextbezogene Antworten**: Der Chatbot behält den Kontext der Unterhaltung bei
- **Responsive Design**: Optimierte Benutzeroberfläche für Desktop und Mobile
- **Produktempfehlungen**: Erhält angepasste Empfehlungen basierend auf Benutzeranfragen
- **Echtzeit-Kommunikation**: Schnelle API-basierte Kommunikation zwischen Frontend und Backend

## Projektstruktur

```
ipa-chatbot/
├── backend/
│   ├── src/
│   │   ├── config/        # Anwendungskonfiguration
│   │   ├── database/      # ChromaDB-Integration
│   │   ├── models/        # Pydantic-Modelle
│   │   ├── routes/        # API-Endpunkte
│   │   ├── services/      # Service-Anbieter
│   │   ├── utils/         # Hilfsfunktionen
│   │   └── data/          # Daten und Prompts
│   ├── main.py            # FastAPI-Anwendungseinstiegspunkt
│   └── requirements.txt   # Python-Abhängigkeiten
├── frontend/
│   ├── public/            # Statische Assets
│   ├── src/
│   │   ├── components/    # React-Komponenten
│   │   ├── pages/         # React-Seiten
│   │   ├── services/      # API-Service-Layer
│   │   └── styles/        # CSS-Styles
│   ├── package.json       # npm-Abhängigkeiten
│   └── README.md          # Frontend-Dokumentation
├── environment.yml        # Conda-Umgebungsdefinition
├── .env                   # Umgebungsvariablen
├── .gitignore             # Git-Ignore-Datei
└── README.md              # Projektdokumentation

## Installation und Setup

### Voraussetzungen

- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda oder Anaconda)
- [Node.js](https://nodejs.org/) (bereits in der Conda-Umgebung enthalten)

### Umgebung einrichten

1. **Repository klonen:**
   ```bash
   git clone https://github.com/CatchMrC/it-hardware-chatbot.git
   cd IPA-chatbot
   ```

2. **Conda-Umgebung erstellen:**
   ```bash
   conda env create -f environment.yml
   ```

3. **Umgebung aktivieren:**
   ```bash
   conda activate ipa-chatbot
   ```

4. **Frontend-Abhängigkeiten installieren:**
   ```bash
   cd frontend
   npm install
   ```

5. **Umgebungsvariablen konfigurieren:**
   - Erstelle eine `.env`-Datei im Hauptverzeichnis basierend auf den Anforderungen des Projekts.

### Anwendung starten

1. **Backend starten:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Frontend starten (in einem separaten Terminal):**
   ```bash
   cd frontend
   npm start
   ```

3. **Öffnen Sie die Anwendung:**
   - Die Anwendung ist nun unter http://localhost:3000 verfügbar
   - Die API-Dokumentation ist unter http://localhost:8000/docs verfügbar

## Umgebung exportieren/importieren

- **Umgebung in eine YAML-Datei exportieren:**
  ```bash
  conda env export > environment.yml
  ```

- **Umgebung aus einer YAML-Datei erstellen:**
  ```bash
  conda env create -f environment.yml
  ```

## Technologien

### Backend
- **FastAPI**: Modernes, schnelles Python-Web-Framework
- **ChromaDB**: Vektordatenbank für semantische Suche
- **Sentence Transformers**: NLP-Modelle für Textvektorisierung
- **Pydantic**: Datenvalidierung und -serialisierung

### Frontend
- **React**: JavaScript-Bibliothek für Benutzeroberflächen
- **Axios**: HTTP-Client für API-Aufrufe
- **React Router**: Routing für React-Anwendungen
- **Bootstrap**: CSS-Framework für responsives Design

## API-Dokumentation

Die API-Dokumentation ist automatisch generiert und kann unter http://localhost:8000/docs aufgerufen werden, wenn das Backend gestartet ist.

### Hauptendpunkte

- **POST /api/chat/message**: Sendet eine Nachricht an den Chatbot
- **GET /api/health**: Überprüft den Status des Servers
- **GET /api/products/search**: Sucht nach Produkten basierend auf Suchbegriffen

## Entwicklung und Beiträge

### Code-Stil und Linting

- **Backend**: Verwende [Black](https://black.readthedocs.io/) für Python-Code-Formatierung
- **Frontend**: Verwende [Prettier](https://prettier.io/) für JavaScript-Code-Formatierung

### Testen

- Führe die Tests für das Backend aus:
  ```bash
  cd backend
  pytest
  ```

- Führe die Tests für das Frontend aus:
  ```bash
  cd frontend
  npm test
  ```

## Ressourcen

- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [React Dokumentation](https://reactjs.org/)
- [ChromaDB Dokumentation](https://docs.trychroma.com/)
- [Sentence Transformers Dokumentation](https://www.sbert.net/)

## UI-Ressourcen

- [Favicon erstellen](https://vectorpaint.yaks.co.nz/) - SVG erstellen
- [Favicon konvertieren](https://favicon.io/favicon-converter/) - ICO erstellen

## Benutzeranleitung

Diese Anleitung hilft Benutzern, den IPA-Chatbot effektiv zu nutzen, um IT-Hardware-Produkte zu finden und Fragen zu beantworten.

### Erste Schritte

1. **Zugang zur Anwendung**
   - Öffnen Sie einen Webbrowser und navigieren Sie zu: `http://localhost:3000` (lokale Entwicklung) oder zur URL der gehosteten Anwendung
   - Die Startseite des Chatbots wird angezeigt

2. **Benutzeroberfläche kennenlernen**
   - **Chatbereich**: Der Hauptbereich zum Anzeigen von Nachrichten
   - **Eingabefeld**: Am unteren Rand der Seite für die Eingabe von Fragen oder Anfragen
   - **Seitenleiste**: Enthält frühere Gespräche und Funktionen

### Produkte suchen

1. **Natürlichsprachige Anfragen**
   - Beschreiben Sie, was Sie suchen, z.B.:
     - "Ich brauche einen leistungsstarken Laptop für Videobearbeitung"
     - "Welcher Monitor eignet sich für Grafikdesign?"
     - "Zeige mir Netzwerk-Router unter 100 Euro"

2. **Produktempfehlungen erhalten**
   - Der Chatbot analysiert Ihre Anfrage und zeigt passende Produkte an
   - Produktkarten enthalten wichtige Informationen wie:
     - Produktname und Bild
     - Technische Spezifikationen
     - Preisinformationen
     - Verfügbarkeit

3. **Produktdetails anzeigen**
   - Klicken Sie auf ein Produkt, um weitere Details zu sehen
   - Bei Bedarf können Sie nach zusätzlichen Informationen zum Produkt fragen

### Fragen stellen

1. **Allgemeine IT-Fragen**
   - Stellen Sie Fragen zu IT-Themen, z.B.:
     - "Was ist der Unterschied zwischen HDD und SSD?"
     - "Wie viel RAM brauche ich für Videobearbeitung?"
     - "Erkläre mir, was ein Firewall macht"

2. **Kontextbezogene Folgefragen**
   - Der Chatbot behält den Kontext des Gesprächs bei
   - Sie können Folgefragen stellen, ohne den Kontext erneut zu erklären, z.B.:
     - "Wie lange halten diese Festplatten?"
     - "Was ist besser für mein Budget?"

### Tipps für die effektive Nutzung

1. **Spezifische Anfragen**
   - Je spezifischer Ihre Anfrage, desto gezielter kann der Chatbot antworten
   - Erwähnen Sie wichtige Kriterien wie Budget, Verwendungszweck oder erforderliche Spezifikationen

2. **Gespräche fortsetzen**
   - Frühere Gespräche können über die Seitenleiste wieder aufgenommen werden
   - Der Chatbot erinnert sich an den Kontext früherer Interaktionen

3. **Feedback geben**
   - Bei unzureichenden Antworten können Sie Ihre Frage umformulieren
   - Spezifischere Anfragen führen oft zu besseren Ergebnissen

### Fehlerbehebung

1. **Keine Produkte gefunden**
   - Versuchen Sie, Ihre Anfrage mit anderen Begriffen umzuformulieren
   - Verwenden Sie allgemeinere Beschreibungen oder spezifizieren Sie andere Eigenschaften

2. **Verbindungsprobleme**
   - Überprüfen Sie Ihre Internetverbindung
   - Aktualisieren Sie die Seite und versuchen Sie es erneut

3. **Unerwartete Antworten**
   - Bei irrelevanten Antworten formulieren Sie Ihre Anfrage klarer und spezifischer
   - Der Chatbot lernt aus Interaktionen und verbessert sich kontinuierlich

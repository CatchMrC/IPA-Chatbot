import requests

# URL der LLM-API
api_url = "http://localhost:11434/api/generate"

# Nutzlast für die Anfrage an die LLM-API
payload = {
    "model": "llama3.2:3B",  # Das zu verwendende Modell
    "prompt": "What color is a llama?",  # Eingabeaufforderung für das Modell
    "stream": False,  # Streaming deaktivieren
    "options": {
        "temperature": 0.7,  # Temperatur für die Antwortgenerierung (Steuerung der Kreativität)
        "top_p": 0.9,  # Top-p-Sampling-Wert
        "num_predict": 500  # Maximale Anzahl der vorhergesagten Token
    }
}

# Senden der POST-Anfrage an die LLM-API
response = requests.post(api_url, json=payload)

# Überprüfung der Antwort
if response.status_code == 200:
    # Erfolgreiche Antwort verarbeiten
    llm_response = response.json()
    print("LLM Response:", llm_response.get("response", "No response found"))
else:
    # Fehler ausgeben, falls die Anfrage fehlschlägt
    print(f"Error: {response.status_code}, {response.text}")
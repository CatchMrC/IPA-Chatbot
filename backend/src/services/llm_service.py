from typing import Dict, Any
import requests
import logging
from pathlib import Path
from jinja2 import Template
from ..config.config import settings


class LLMService:
    def __init__(self):
        # Initialisiert den LLM-Service mit API-URL und Modell
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL
        self.conversation_history = []  # Verlauf der Konversationen

    async def generate_response(self, message: str, role_type: str = "general", context: Dict = None) -> Dict[str, str]:
        """
        Generiert eine Antwort basierend auf der Eingabe des Benutzers.

        :param message: Die Nachricht des Benutzers.
        :param role_type: Der Typ der Rolle (z. B. "general" oder "product_specific").
        :param context: Zusätzlicher Kontext für die Antwortgenerierung.
        :return: Ein Dictionary mit der generierten Antwort oder einem Fehler.
        """
        try:
            # Erstellt den Prompt basierend auf Rolle und Kontext
            prompt = self._get_prompt(role_type, message, context)
            
            # Anfrage an die LLM-API senden
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": settings.LLM_TEMPERATURE,
                        "top_p": 0.9,
                        "num_predict": 512
                    }
                }
            )

            # Erfolgreiche Antwort verarbeiten
            if response.status_code == 200:
                llm_response = response.json()["response"].strip()
                self._update_conversation_history(message, llm_response)
                return {"response": llm_response}

            # Fehlerhafte Antwort zurückgeben
            return {"error": f"LLM-Anfrage fehlgeschlagen mit Status {response.status_code}"}

        except Exception as e:
            # Fehler bei der Antwortgenerierung behandeln
            return {"error": f"Fehler bei der Antwortgenerierung: {str(e)}"}

    def _get_prompt(self, role_type: str, message: str, context: Dict = None) -> str:
        """
        Erstellt den Prompt basierend auf der Rolle und dem Kontext.

        :param role_type: Der Typ der Rolle (z. B. "general" oder "product_specific").
        :param message: Die Nachricht des Benutzers.
        :param context: Zusätzlicher Kontext für die Antwortgenerierung.
        :return: Der generierte Prompt als String.
        """
        context = context or {}
        
        # Formatierung des Konversationsverlaufs
        recent_history = self._format_history(self.conversation_history[-4:]) if self.conversation_history else ""
        
        # Unterschiedliche Modi basierend auf der Rolle
        if role_type == "product_specific" and context and "product" in context:
            product = context['product']
            return self._load_prompt("product_specific", {
                **product,
                "history": recent_history,
                "message": message
            })
        else:
            # Standardmodus: Allgemeiner IT-Chat
            return self._load_prompt("general", {
                "history": recent_history,
                "message": message
            })

    def _load_prompt(self, prompt_type: str, params: dict) -> str:
        """
        Lädt und rendert den Prompt basierend auf einem Jinja2-Template.

        :param prompt_type: Der Typ des Prompts (z. B. "general" oder "product_specific").
        :param params: Parameter, die in das Template eingefügt werden.
        :return: Der gerenderte Prompt als String.
        """
        try:
            prompts_path = Path(__file__).parent.parent / "prompts" / f"{prompt_type}.jinja2"
            with open(prompts_path, 'r', encoding='utf-8') as f:
                template = Template(f.read())
            return template.render(**params)
        except Exception as e:
            print(f"Fehler beim Rendern des Prompts '{prompt_type}': {e}")
            return f"Error: {e}"

    def _format_history(self, history: list) -> str:
        """
        Formatiert den Konversationsverlauf für die Verwendung im Prompt.

        :param history: Eine Liste von Nachrichten im Verlauf.
        :return: Der formatierte Verlauf als String.
        """
        return "\n".join([
            f"{'User' if m['type'] == 'user' else 'Assistant'}: {m['content']}"
            for m in history
        ])

    def _update_conversation_history(self, user_message: str, ai_response: str):
        """
        Aktualisiert den Konversationsverlauf mit der neuesten Nachricht und Antwort.

        :param user_message: Die Nachricht des Benutzers.
        :param ai_response: Die Antwort des KI-Modells.
        """
        self.conversation_history.append({"type": "user", "content": user_message})
        self.conversation_history.append({"type": "assistant", "content": ai_response})
        self.conversation_history = self.conversation_history[-10:]  # Nur die letzten 10 Nachrichten behalten

    def reset_conversation(self) -> Dict[str, str]:
        """
        Setzt den Konversationsverlauf zurück.

        :return: Eine Bestätigung, dass der Verlauf zurückgesetzt wurde.
        """
        self.conversation_history = []
        return {"response": "Conversation has been reset."}
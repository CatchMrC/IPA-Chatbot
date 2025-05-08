from typing import Dict, Any, List, Optional
import requests
import logging
from pathlib import Path
import os
from jinja2 import Template
from ..config.config import settings

class LLMService:
    def __init__(self):
        self.api_url = settings.LLM_API_URL  # URL der LLM-API
        self.model = settings.LLM_MODEL  # Verwendetes Modell
        self.conversation_history = []  # Verlauf der Konversation
        self._initialize_templates()  # Initialisiere die Vorlagen

    def _initialize_templates(self):
        """Initialisiere die Prompt-Vorlagen"""
        self.templates = {
            "general": self._load_template_from_file("general"),
            "productSpecific": self._load_template_from_file("product_specific"),
            "productRecommendation": self._load_template_from_file("product_recommendation"),
            "orderInstructions": self._load_template_from_file("order_instructions"),
            "clarification": self._load_template_from_file("clarification"),
        }

    def _load_template_from_file(self, template_name: str) -> str:
        """Lade eine Vorlage aus einer Datei oder verwende eine Standardvorlage"""
        template_path = settings.DATA_DIR / "prompts" / f"{template_name}.txt"
        
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
                
        # Standardvorlage verwenden, falls Datei nicht existiert
        defaults = {
            "general": """
Du bist ein IT-Hardware-Berater. Sei hilfsbereit, kompetent und gesprächig.
{{ history }}
Benutzer: {{ message }}
Assistent:""",
            "product_specific": """
Du bist ein IT-Hardware-Produktspezialist. Analysiere und erkläre die Eigenschaften, Vorteile und Nachteile des Produkts.
Produkt: {{ manufacturer }} {{ model }}
Typ: {{ header.type }}
Preis: {{ header.price }}
{{ history }}
Benutzer: {{ message }}
Assistent:""",
            "product_recommendation": """
Du bist ein IT-Hardware-Empfehlungsspezialist. Empfehle geeignete Produkte basierend auf den Anforderungen des Benutzers.
{{ history }}
Benutzeranforderungen: {{ user_requirements }}
Benutzer: {{ message }}
Assistent:""",
            "order_instructions": """
Du bist ein IT-Hardware-Bestellassistent. Gib klare Anweisungen, wie das Produkt bestellt oder gekauft werden kann.
Produkt: {{ manufacturer }} {{ model }}
{{ history }}
Benutzeranfrage: {{ user_query }}
Assistent:""",
            "clarification": """
Du bist ein IT-Hardware-Berater. Stelle klärende Fragen, um die Bedürfnisse des Benutzers besser zu verstehen.
{{ history }}
Benutzer: {{ message }}
Assistent:"""
        }
        
        # Erstelle das Verzeichnis für Vorlagen, falls es nicht existiert
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        
        # Speichere die Standardvorlage für zukünftige Verwendung
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(defaults.get(template_name, defaults["general"]))
            
        return defaults.get(template_name, defaults["general"])

    async def generate_response(self, message: str, role_type: str = "general", context: Dict = None) -> Dict[str, str]:
        """Generiere eine Antwort vom LLM"""
        try:
            prompt = self._get_prompt(role_type, message, context)
            logging.info(f"Sende Anfrage an LLM: URL={self.api_url}, Modell={self.model}")

            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": settings.LLM_TEMPERATURE,
                        "top_p": 0.9,
                        "num_predict": settings.LLM_MAX_TOKENS
                    }
                }
            )

            if response.status_code == 200:
                llm_response = response.json()["response"].strip()
                self._update_conversation_history(message, llm_response)
                return {"response": llm_response}
            
            error_msg = f"LLM-Anfrage fehlgeschlagen mit Status {response.status_code}"
            logging.error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Fehler bei der Generierung der Antwort: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}

    def _get_prompt(self, role_type: str, message: str, context: Dict = None) -> str:
        """Erstelle den Prompt basierend auf der Rolle und dem Kontext"""
        context = context or {}
        
        # Prüfe, ob es sich um eine bestellbezogene Anfrage handelt
        is_order_query = self._is_order_related_query(message)
        
        # Überschreibe die Rolle für bestellbezogene Anfragen
        if is_order_query:
            role_type = "orderInstructions"
            context["user_query"] = message
            
            # Produktinformationen zum Kontext hinzufügen, falls verfügbar
            if "product" in context:
                context["manufacturer"] = context["product"].get("manufacturer", "")
                context["model"] = context["product"].get("model", "")
            
            # Verlauf formatieren, falls verfügbar
            if "history" in context and context["history"]:
                context["history"] = self._format_history(context["history"])
            
            return self._render_template("orderInstructions", context)
        
        # Konversationsverlauf formatieren
        recent_history = self._format_history(self.conversation_history[-4:]) if self.conversation_history else ""
        
        # Unterschiedliche Rollentypen behandeln
        if role_type == "product_specific" and context:
            product = context.get('product', {})
            return self._render_template("productSpecific", {
                **product,
                "history": recent_history,
                "message": message
            })
        elif role_type == "recommendation":
            return self._render_template("productRecommendation", {
                "user_requirements": context.get("user_requirements", ""),
                "history": recent_history,
                "message": message
            })
        elif role_type == "clarification":
            return self._render_template("clarification", {
                "history": recent_history,
                "message": message
            })
            
        # Standard: Allgemeine Konversation
        return self._render_template("general", {
            "history": recent_history,
            "message": message
        })
    
    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Rendere eine Vorlage mit dem gegebenen Kontext"""
        template = self.templates.get(template_name, self.templates["general"])
        return Template(template).render(**context)
    
    def _is_order_related_query(self, message: str) -> bool:
        """Bestimme, ob eine Nachricht mit einer Bestellung zusammenhängt"""
        order_keywords = [
            "bestellen", "kaufen", "order", "purchase", "buy", "acquire", 
            "get this", "where can i get", "wie kann ich kaufen", "wie bestelle ich"
        ]
        
        lower_message = message.lower()
        return any(keyword in lower_message for keyword in order_keywords)
        
    def _format_history(self, history) -> str:
        """Formatiere den Konversationsverlauf für Prompts"""
        if not history:
            return ""
            
        formatted = "\n--- KONVERSATIONSVERLAUF ---\n"
        for entry in history:
            formatted += f"Benutzer: {entry.get('user', '')}\n"
            formatted += f"Assistent: {entry.get('assistant', '')}\n\n"
        return formatted
        
    def _update_conversation_history(self, user_message: str, assistant_response: str) -> None:
        """Aktualisiere den Konversationsverlauf mit neuen Nachrichten"""
        self.conversation_history.append({
            "user": user_message,
            "assistant": assistant_response
        })
        
        # Begrenze die Länge des Verlaufs
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
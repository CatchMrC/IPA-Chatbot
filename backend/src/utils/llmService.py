from typing import Dict, Any, List, Optional
import requests
import logging
from pathlib import Path
import os
from jinja2 import Template
from ..config.config import settings

class LLMService:
    def __init__(self):
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL
        self.conversation_history = []
        self._initialize_templates()

    def _initialize_templates(self):
        """Initialisiere die Vorlagen für Prompts"""
        self.templates = {
            "general": self._load_template_from_file("general"),
            "productSpecific": self._load_template_from_file("product_specific"),
            "productRecommendation": self._load_template_from_file("product_recommendation"),
            "orderInstructions": self._load_template_from_file("order_instructions")
        }

    def _load_template_from_file(self, template_name: str) -> str:
        """Lade eine Vorlage aus einer Datei oder verwende eine Standardvorlage"""
        # Prüfe, ob die Vorlagendatei existiert
        template_path = settings.DATA_DIR / "prompts" / f"{template_name}.jinja2"
        
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
                
        # Wenn die Vorlagendatei nicht existiert, gib eine Warnung aus und gib eine leere Vorlage zurück
        logging.warning(f"Template file {template_name}.jinja2 not found. Please create it in {template_path}")
        return f"Template {template_name} not found. Please create it in {template_path}"

    async def generate_response(self, message: str, role_type: str = "general", context: Dict = None) -> Dict[str, str]:
        """Generiere eine Antwort vom LLM"""
        try:
            prompt = self._get_prompt(role_type, message, context)
            logging.info(f"Sending request to LLM: URL={self.api_url}, Model={self.model}")

            # Füge Systemanweisung hinzu, die das Verhalten des LLM steuert
            system_instruction = """You are a friendly IT hardware advisor from Novartis. Your main focus is on IT topics and products.

For IT product inquiries: ONLY discuss products that are in the Novartis product database.

For general questions: You may politely and competently answer non-IT related questions, but indicate at the end of your response that you're primarily available for IT-related matters."""
            
            is_first_message = len(self.conversation_history) == 0
            system_instruction += f"\nNOTE: This is {'the first' if is_first_message else 'NOT the first'} message in the conversation. {'You may greet the user once.' if is_first_message else 'DO NOT start with a greeting.'}"
            
            full_prompt = f"{system_instruction}\n\n{prompt}"

            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": full_prompt,
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
            
            error_msg = f"LLM request failed with status {response.status_code}"
            logging.error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}

    def _get_prompt(self, role_type: str, message: str, context: Dict = None) -> str:
        """Erstelle einen Prompt basierend auf Rolle und Kontext"""
        context = context or {}
        
        # Prüfe, ob es sich um eine bestellungsbezogene Anfrage handelt
        is_order_query = self._is_order_related_query(message)
        
        # Überschreibe den Rollentyp für bestellungsbezogene Anfragen
        if is_order_query and "product" in context:
            role_type = "orderInstructions"
            context["user_query"] = message
            
            # Füge Produktinformationen zum Kontext hinzu, falls verfügbar
            if "product" in context:
                product = context["product"]
                context["manufacturer"] = product.get("header", {}).get("manufacturer", "")
                context["model"] = product.get("header", {}).get("model", "")
            
            # Formatiere den Verlauf, falls verfügbar
            if "history" in context and context["history"]:
                context["history"] = self._format_history(context["history"])
            
            return self._render_template("orderInstructions", context)
        
        # Formatiere den Gesprächsverlauf
        recent_history = self._format_history(self.conversation_history[-4:]) if self.conversation_history else ""
        
        # Behandle verschiedene Rollentypen
        if role_type == "product_specific" and context and "product" in context:
            product = context["product"]
            header = product.get("header", {})
            
            return self._render_template("productSpecific", {
                "manufacturer": header.get("manufacturer", ""),
                "model": header.get("model", ""),
                "type": header.get("type", ""),
                "price": header.get("price", ""),
                "environment": header.get("environment", ""),
                "specifications": product.get("specifications", {}),
                "users": product.get("target_audience", {}),
                "link": product.get("link", ""),
                "history": recent_history,
                "message": message
            })
        elif role_type == "recommendation":
            # Stelle sicher, dass verfügbare Produkte im Kontext sind
            if "available_products" not in context and "products" in context:
                # Formatiere Produkte in einem lesbaren Format
                products_text = self._format_products_for_context(context["products"])
                context["available_products"] = products_text
            
            return self._render_template("productRecommendation", {
                "user_requirements": context.get("user_requirements", ""),
                "available_products": context.get("available_products", "No products available"),
                "history": recent_history,
                "message": message,
                "single_product": context.get("single_product", True)  # Flag aus dem neuen Code
            })          
        # Standard: Allgemeine Konversation
        return self._render_template("general", {
            "system_context": context.get("system_context", ""),
            "history": recent_history,
            "message": message
        })
    
    def _format_products_for_context(self, products: List[Dict]) -> str:
        """Formatiere eine Liste von Produkten für den LLM-Kontext"""
        if not products:
            return "No products available"
            
        formatted = []
        for i, p in enumerate(products):
            header = p.get("header", {})
            specs = p.get("specifications", {}).get("system", {})
            
            product_text = f"Product {i+1}: {header.get('manufacturer', 'Unknown')} {header.get('model', 'Unknown')}\n"
            product_text += f"  Type: {header.get('type', 'N/A')}\n"
            product_text += f"  Price: {header.get('price', 'N/A')}\n"
            
            # Add specifications
            if specs:
                product_text += "  Specifications:\n"
                for key, value in specs.items():
                    if value and value != "N/A":
                        product_text += f"    - {key}: {value}\n"
            
            formatted.append(product_text)
        
        return "\n".join(formatted)
    
    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Rendere eine Vorlage mit dem gegebenen Kontext"""
        template = self.templates.get(template_name, self.templates["general"])
        return Template(template).render(**context)
    
    def _is_order_related_query(self, message: str) -> bool:
        """Ermittle, ob eine Nachricht mit einer Bestellung zusammenhängt"""
        order_keywords = [
            "order", "purchase", "buy", "get", "acquire", "request", 
            "availability", "stock", "place an order", "delivery", 
            "shipping", "lead time", "bestellen", "kaufen", "erwerben",
            "verfügbarkeit", "lieferung", "bestellung", "einkaufen",
            "where can i get", "wie kann ich kaufen", "wie bestelle ich"
        ]
        
        lower_message = message.lower()
        return any(keyword in lower_message for keyword in order_keywords)
        
    def _format_history(self, history) -> str:
        """Formatiere den Gesprächsverlauf für Prompts"""
        if not history:
            return ""
            
        formatted = "\n--- CONVERSATION HISTORY ---\n"
        
        # Behandle beide Verlaufsformate (alt und neu)
        if isinstance(history, list) and history and isinstance(history[0], dict):
            if "type" in history[0]:  # Neues Format
                for entry in history:
                    formatted += f"{'User' if entry.get('type') == 'user' else 'Assistant'}: {entry.get('content', '')}\n"
            else:  # Altes Format
                for entry in history:
                    formatted += f"User: {entry.get('user', '')}\n"
                    formatted += f"Assistant: {entry.get('assistant', '')}\n\n"
                    
        return formatted
        
    def _update_conversation_history(self, user_message: str, assistant_response: str) -> None:
        """Aktualisiere den Gesprächsverlauf mit neuen Nachrichten"""
        # Verwende das neue Format
        self.conversation_history.append({"type": "user", "content": user_message})
        self.conversation_history.append({"type": "assistant", "content": assistant_response})
        
        # Begrenze die Verlaufslänge
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
            
    def reset_conversation(self) -> Dict[str, str]:
        """Setze den Gesprächsverlauf zurück"""
        self.conversation_history = []
        return {"response": "Conversation has been reset."}
from typing import Dict, Any, List

class ProductFormatter:
    @staticmethod
    def _parse_tech_specs(tech_specs: str) -> Dict[str, str]:
        """Parsiere technische Spezifikationen in ein strukturiertes Format"""
        specs_dict = {}
        if not tech_specs:
            return specs_dict

        # Verschachtelte Kommas innerhalb der Spezifikationen behandeln
        specs_list = []
        current_spec = []
        in_parentheses = False

        for char in tech_specs:
            if char == '(' or char == '[':
                in_parentheses = True
            elif char == ')' or char == ']':
                in_parentheses = False
            
            if char == ',' and not in_parentheses:
                specs_list.append(''.join(current_spec))
                current_spec = []
            else:
                current_spec.append(char)
        
        if current_spec:
            specs_list.append(''.join(current_spec))

        # Jede Spezifikation analysieren
        for spec in specs_list:
            if ':' in spec:
                key, value = spec.split(':', 1)
                specs_dict[key.strip()] = value.strip()

        return specs_dict

    @staticmethod
    def _clean_list(value: str) -> List[str]:
        """Bereinige und teile einen String in eine Liste auf, unter Berücksichtigung von Kommas und Zeilenumbrüchen"""
        if not value or value == 'N/A':
            return []
        # Sowohl nach Zeilenumbrüchen als auch nach Kommas aufteilen
        items = [item.strip() for item in value.replace('\n', ',').split(',')]
        return [item for item in items if item]

    @staticmethod
    def format_product(metadata: Dict[str, Any], product_id: str) -> Dict[str, Any]:
        """Formatiere die Metadaten eines Produkts in ein strukturiertes Format"""
        # Modellname bereinigen
        model = metadata.get('model', 'N/A').replace('\n', ' ').strip()
        manufacturer = metadata.get('manufacturer', '')
        
        return {
            "id": product_id,
            "header": {
                "manufacturer": manufacturer,
                "model": model,
                "name": f"{manufacturer} {model}".strip(),
                "type": metadata.get('type', 'N/A'),
                "price": metadata.get('price_chf', 'N/A'),
                "link": metadata.get('link', 'N/A')
            },
            "target_audience": {
                "users": ProductFormatter._clean_list(metadata.get('user_profile', '')),
                "ideal_for": ProductFormatter._clean_list(metadata.get('ideal_for', '')),
                "not_recommended": ProductFormatter._clean_list(metadata.get('not_recommended_for', '')),
                "qualification": metadata.get('qualification', 'N/A')
            },
            "specifications": {
                "system": ProductFormatter._parse_tech_specs(metadata.get('tech_specs', '')),
                "os": metadata.get('os', 'N/A').strip()
            },
            "metadata": {
                "id": product_id,
                "qualification": metadata.get('qualification', 'N/A'),
                "last_updated": metadata.get('last_updated', 'N/A')
            }
        }

    @staticmethod
    def format_price_text(price: Any) -> str:
        """Formatiere den Preis für die Anzeige"""
        if not price or price == 'N/A':
            return "Preis auf Anfrage"
        if isinstance(price, str) and price.upper() == 'PCLCM':
            return "Preis auf Anfrage (PCLCM)"
        return f"CHF {price}"
        
    @staticmethod
    def format_search_result(products: List[Dict[str, Any]], message: str = None) -> Dict[str, Any]:
        """Formatiere Suchergebnisse für die API-Antwort"""
        return {
            "products": products,
            "count": len(products),
            "message": message if message else f"{len(products)} passende Produkte gefunden"
        }
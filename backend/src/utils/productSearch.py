from typing import Dict, Any, List
from ..database.chromadbClient import ChromaDBClient
from .textAnalyzer import TextAnalyzer
from .productFormatter import ProductFormatter

class ProductSearch:
    def __init__(self):
        self.db_client = ChromaDBClient()  # Datenbank-Client für Produktsuche
        self.text_analyzer = TextAnalyzer()  # Textanalyse-Tool
        self.formatter = ProductFormatter()  # Formatter für Produktdaten

    def search(self, query: str) -> Dict[str, Any]:
        """Einfache Produktsuche mit Debug-Ausgabe"""
        try:
            print(f"[DEBUG] 🔍 Anfrage erhalten: {query}")
            # Erstelle Embedding für die Anfrage
            query_embedding = self.text_analyzer.get_embedding(query)
            # Suche Produkte in der Datenbank
            results = self.db_client.search_products(query_embedding)

            # Debug: Anzahl der Ergebnisse und Beispiel-Metadaten
            print(f"[DEBUG] ✅ ChromaDB Ergebnisanzahl: {len(results['metadatas'][0])}")
            for idx, meta in enumerate(results["metadatas"][0][:3]):
                print(f"[DEBUG] ➤ Metadaten {idx+1}:", meta)

            # Formatiere die gefundenen Produkte
            products = [
                self.formatter.format_product(metadata, results["ids"][0][idx])
                for idx, metadata in enumerate(results["metadatas"][0])
            ]

            print(f"[DEBUG] 📦 Formatierte Produkte (erstes 1): {products[:1]}")  # Zeigt 1 Beispielprodukt
            return self.formatter.format_search_result(products)

        except Exception as e:
            print(f"[ERROR] ❌ Suche fehlgeschlagen: {str(e)}")
            return self.formatter.format_search_result(
                [],
                f"Fehler bei der Suche: {str(e)}"
            )

    def search_with_advice(self, query: str, single_product: bool = True) -> Dict[str, Any]:
        """Produktsuche mit Empfehlungen"""
        try:
            # Erstelle Embedding für die Anfrage
            query_embedding = self.text_analyzer.get_embedding(query)
            # Suche Produkte in der Datenbank
            results = self.db_client.search_products(query_embedding)

            # Formatiere die gefundenen Produkte
            products = [
                self.formatter.format_product(metadata, results["ids"][0][idx])
                for idx, metadata in enumerate(results["metadatas"][0])
            ]

            if not products:
                return self.formatter.format_search_result(
                    [],
                    "Es wurden keine passenden Produkte gefunden. Bitte versuchen Sie es mit anderen Suchbegriffen."
                )

            # Limitiere die Anzahl der Produkte basierend auf dem Parameter single_product
            product_limit = 1 if single_product else 5
            products_to_show = products[:product_limit]
            
            # Erstelle eine detaillierte Empfehlungsnachricht
            if single_product:
                message = "Basierend auf Ihren Anforderungen empfehle ich dieses Produkt:\n"
            else:
                message = "Basierend auf Ihren Anforderungen empfehle ich diese Produkte:\n"
                
            for idx, product in enumerate(products_to_show, 1):
                header = product["header"]
                specs = product["specifications"]["system"]
                target = product["target_audience"]

                message += f"\n{idx}. {header['name']} ({self.formatter.format_price_text(header['price'])})"
                message += f"\n   Typ: {header['type']}"

                # Wichtige Spezifikationen hinzufügen, falls verfügbar
                if specs:
                    key_specs = []
                    if 'RAM' in specs:
                        key_specs.append(f"RAM: {specs['RAM']}")
                    if 'CPU' in specs:
                        key_specs.append(f"CPU: {specs['CPU']}")
                    if 'Storage' in specs:
                        key_specs.append(f"Speicher: {specs['Storage']}")
                    if key_specs:
                        message += f"\n   Spezifikationen: {', '.join(key_specs)}"
                
                # Zielgruppe hinzufügen, falls verfügbar
                if target["ideal_for"]:
                    message += f"\n   Ideal für: {', '.join(target['ideal_for'][:2])}"
                
            return {
                "products": products_to_show,
                "count": len(products_to_show),
                "message": message
            }
            
        except Exception as e:
            print(f"[ERROR] ❌ Empfehlungssuche fehlgeschlagen: {str(e)}")
            return self.formatter.format_search_result(
                [],
                "Entschuldigung, es gab ein Problem bei der Suche nach Empfehlungen."
            )
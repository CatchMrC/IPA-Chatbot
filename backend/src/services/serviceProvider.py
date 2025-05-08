from src.utils.llmService import LLMService
from src.utils.productSearch import ProductSearch

# Erstelle Service-Instanzen als Singletons, um sie wiederzuverwenden
llm_service = LLMService()  # Instanz des LLM-Dienstes
product_search = ProductSearch()  # Instanz des Produktsuchdienstes

# Getter-Funktion fuer den LLM-Service (fuer Dependency Injection)
def get_llm_service():
    return llm_service

# Getter-Funktion fuer den Produktsuchdienst (fuer Dependency Injection)
def get_product_search():
    return product_search
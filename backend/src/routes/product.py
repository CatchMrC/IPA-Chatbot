from fastapi import APIRouter, HTTPException, Depends
from src.models.product import ProductQuery
from src.utils.llmService import LLMService
from src.utils.productSearch import ProductSearch
from src.services.serviceProvider import get_llm_service, get_product_search

router = APIRouter(tags=["products"])

@router.post("/api/search")
async def search(
    query: ProductQuery, 
    product_search: ProductSearch = Depends(get_product_search)
):
    """Search for products with optional advice"""
    try:
        if query.include_advice:
            # Änderung hier: single_product=True explizit übergeben
            return product_search.search_with_advice(query.query, single_product=True)
        return product_search.search(query.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/recommendation")
async def recommend(
    query: ProductQuery,
    product_search: ProductSearch = Depends(get_product_search),
    llm_service: LLMService = Depends(get_llm_service)
):
    try:
        # 1. Produkte aus ChromaDB abrufen
        search_result = product_search.search(query.query)
        products = search_result["products"]

        if not products:
            raise HTTPException(status_code=404, detail="No products found.")

        # Top 3-5 Produkte auswählen, aus denen das LLM wählen kann
        top_products = products[:3]  # Auf 3 Optionen für das LLM beschränken
        
        # 2. Produkte für den Prompt formatieren
        formatted_products = []
        for i, p in enumerate(top_products):
            product_name = f"{p['header'].get('manufacturer', 'Unknown')} {p['header'].get('model', 'Unknown')}"
            product_id = i  # Index als Produkt-ID verwenden
            
            formatted_products.append(
                f"Product {product_id}: {product_name} - "
                f"{p['specifications']['system'].get('ram', '')}, "
                f"{p['specifications']['system'].get('cpu', '')}, "
                f"{p['specifications']['system'].get('storage', '')} | "
                f"{p['header'].get('price', 'N/A')}€, {p['header'].get('type', 'N/A')}"
            )
        
        formatted_products_text = "\n".join(formatted_products)

        # 3. LLM-Kontext vorbereiten
        context = {
            "user_requirements": query.query,
            "available_products": formatted_products_text,
            "history": "",
            "message": "Which product would you recommend and why? Start your response with 'SELECTED_PRODUCT_ID: X' where X is the product number you recommend.",
            "single_product": True
        }

        # 4. LLM-Antwort generieren
        response = await llm_service.generate_response(
            message=context["message"],
            role_type="recommendation",
            context=context
        )

        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])

        llm_response = response["response"]
        
        # 5. Ausgewählte Produkt-ID aus der LLM-Antwort extrahieren
        selected_product_id = 0  # Standardmässig erstes Produkt
        
        # Nach dem SELECTED_PRODUCT_ID-Muster suchen
        import re
        pattern = r"SELECTED_PRODUCT_ID:\s*(\d+)"
        match = re.search(pattern, llm_response)
        
        if match:
            try:
                selected_product_id = int(match.group(1))
                # Sicherstellen, dass es im gültigen Bereich liegt
                selected_product_id = min(selected_product_id, len(top_products) - 1)
                # SELECTED_PRODUCT_ID-Zeile aus der Antwort entfernen
                llm_response = re.sub(pattern, "", llm_response).strip()
            except:
                pass  # Bei Konvertierungsfehler Standard verwenden
        
        # 6. Nur das ausgewählte Produkt zurückgeben
        selected_product = top_products[selected_product_id]
        
        return {
            "recommended_products": [selected_product],  # Nur das Produkt zurückgeben, das das LLM beschrieben hat
            "llm_response": llm_response
        }
    except Exception as e:
        print("[ERROR] ❌ Empfehlung fehlgeschlagen:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
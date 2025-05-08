from fastapi import APIRouter, Depends
from ..models.product import ProductQuery
from ..services.serviceProvider import get_product_search
from ..utils.productSearch import ProductSearch

# Erstelle einen Router mit dem Prefix "/api" und dem Tag "products"
router = APIRouter(
    prefix="/api",
    tags=["products"],
)

@router.post("/search")
async def search_products(query: ProductQuery, 
                         product_search: ProductSearch = Depends(get_product_search)):
    """Suche nach Produkten basierend auf der Anfrage"""
    # Fuehre eine Produktsuche basierend auf der Anfrage durch
    return product_search.search(query.query)

@router.post("/recommendation")
async def get_recommendation(query: ProductQuery, 
                            product_search: ProductSearch = Depends(get_product_search)):
    """Produktempfehlung mit detailliertem LLM-Rat"""
    # Generiere Produktempfehlungen mit oder ohne detaillierten Rat
    return product_search.search_with_advice(query.query, query.include_advice is False)
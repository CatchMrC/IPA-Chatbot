from fastapi import APIRouter, Depends
from ..models.chat import ChatRequest
from ..services.serviceProvider import get_llm_service
from ..utils.llmService import LLMService

# Erstelle einen Router mit dem Prefix "/api" und dem Tag "chat"
router = APIRouter(
    prefix="/api",
    tags=["chat"],
)

@router.post("/chat")
async def chat(request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)):
    """
    Chat-API-Endpunkt fuer allgemeine und produktspezifische Anfragen.
    """
    # Generiere eine Antwort mit Hilfe des LLM-Service
    return await llm_service.generate_response(
        message=request.message,  # Die Nachricht des Benutzers
        role_type=request.role_type or "general",  # Rolle des Benutzers (Standard: "general")
        context=request.context  # Kontext der Anfrage
    )
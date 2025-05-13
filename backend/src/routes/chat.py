from fastapi import APIRouter, HTTPException, Depends
from src.models.chat import ChatRequest
from src.utils.llmService import LLMService
from src.services.serviceProvider import get_llm_service

router = APIRouter(tags=["chat"])

@router.post("/api/chat")
async def chat(request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)):
    """Handle chat requests with optional product context"""
    try:
        # Kontext und Rollentyp initialisieren
        context = {"history": request.history if request.history else []}
        role_type = request.role_type if request.role_type else "general"
        
        # Produktkontext hinzufügen, falls verfügbar
        if request.context and "product" in request.context:
            product = request.context["product"]
            context["product"] = product
            
        # LLM-Antwort generieren
        response = await llm_service.generate_response(
            message=request.message,
            role_type=role_type,
            context=context
        )
            
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/reset-chat")
async def reset_chat(llm_service: LLMService = Depends(get_llm_service)):
    """Reset the chat conversation history"""
    try:
        return llm_service.reset_conversation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
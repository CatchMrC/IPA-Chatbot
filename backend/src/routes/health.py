from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config.config import settings

# Erstelle einen Router mit dem Prefix "/api" und dem Tag "health"
router = APIRouter(
    prefix="/api",
    tags=["health"],
)

@router.get("/health")
async def health_check():
    """
    API-Gesundheitsueberpruefung fuer Monitoring.
    """
    # Rueckgabe des Gesundheitsstatus der API
    return JSONResponse({
        "status": "ok",  # Status der API
        "version": settings.APP_VERSION,  # Aktuelle Version der Anwendung
        "environment": "development" if settings.DEBUG else "production"  # Umgebung (Entwicklung oder Produktion)
    })
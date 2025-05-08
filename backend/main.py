from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings

# Service Provider importieren
# Die Service-Instanzen werden automatisch erstellt beim Import
from src.services.serviceProvider import llm_service, product_search

# Routes importieren
from src.routes import chat, health, product

# Hauptanwendung initialisieren
app = FastAPI()

# CORS-Middleware konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(chat.router)
app.include_router(health.router)
app.include_router(product.router)

# Hauptausführungsblock für lokalen Entwicklungsserver
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Absolute Pfade ermitteln
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"
DATA_DIR = BACKEND_ROOT / "src" / "data"
DB_DIR = BACKEND_ROOT / "db"
ENV_FILE = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Projektstruktur
    PROJECT_ROOT: Path = PROJECT_ROOT
    BACKEND_ROOT: Path = BACKEND_ROOT
    DATA_DIR: Path = DATA_DIR
    DB_DIR: Path = DB_DIR
    
    # LLM-Konfiguration
    LLM_API_URL: str = "http://localhost:11434/api/generate"
    LLM_MODEL: str = "llama3.2:3B"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: Optional[int] = 512
    
    # Server-Konfiguration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Datenbank-Konfiguration
    DB_PATH: Path = DB_DIR / "chromadb_store"
    COLLECTION_NAME: str = "hardware_products"
    
    # Produktsuche-Konfiguration
    PRODUCT_DATA_PATH: Path = DATA_DIR / "itHardware.csv"
    SEARCH_LIMIT: int = 5
    MODEL_NAME: str = "all-MiniLM-L6"

    # Debug-Konfiguration
    DEBUG: bool = True

    # Anwendungsversion
    APP_VERSION: str = "1.0.0"
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_prefix="APP_"
    )

    def setup_directories(self):
        """Create required directories if they don't exist"""
        for directory in [self.DATA_DIR, self.DB_PATH.parent]:
            directory.mkdir(parents=True, exist_ok=True)
            if self.DEBUG:
                print(f"Verzeichnis existiert oder wurde erstellt: {directory}")

# Singleton-Instanz erstellen
settings = Settings()

# Verzeichnisse einrichten
settings.setup_directories()

if settings.DEBUG:
    print("\nConfiguration Settings:")
    print(f"Project Root: {settings.PROJECT_ROOT}")
    print(f"Backend Root: {settings.BACKEND_ROOT}")
    print(f"Data Dir: {settings.DATA_DIR}")
    print(f"DB Path: {settings.DB_PATH}")
    print(f"Collection Name: {settings.COLLECTION_NAME}")
    print(f"Product Data: {settings.PRODUCT_DATA_PATH}")
    print(f"Model: {settings.MODEL_NAME}")    
    print(f"Model: {settings.LLM_MODEL}\n")
"""Configuration management for the AI service."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = "test-key"  # Default for testing
    openai_model: str = "gpt-4-turbo-preview"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    
    # ChromaDB Configuration
    chroma_persist_directory: str = "./chroma_db"
    
    # WordPress Integration
    wordpress_api_url: Optional[str] = None
    wordpress_api_key: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()

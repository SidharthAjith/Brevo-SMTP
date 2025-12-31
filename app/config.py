from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # SMTP Configuration
    smtp_host: str = "smtp-relay.brevo.com"
    smtp_port: int = 587
    smtp_username: EmailStr
    smtp_password: str
    smtp_from_email: EmailStr
    smtp_from_name: str = "BPO Acceptor"
    
    # Recipient
    recipient_email: EmailStr
    
    # Webhook Security
    webhook_secret: Optional[str] = None
    
    # Application Settings
    app_name: str = "BPO Acceptor Lead Service"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a global settings instance
settings = Settings()

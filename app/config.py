from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Brevo API Configuration
    BREVO_API_KEY: str
    BREVO_SENDER_EMAIL: EmailStr
    BREVO_SENDER_NAME: str = "BPO Acceptor"
    
    # Recipients (comma-separated emails in env)
    RECIPIENT_EMAILS: str  # Will be parsed into list
    
    # Webhook Security
    WEBHOOK_SECRET: Optional[str] = None
    
    # Application Settings
    APP_NAME: str = "BPO Acceptor Lead Service"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_recipient_list(self) -> List[str]:
        """Parse comma-separated recipient emails into list."""
        return [email.strip() for email in self.RECIPIENT_EMAILS.split(",")]


# Create a global settings instance
settings = Settings()

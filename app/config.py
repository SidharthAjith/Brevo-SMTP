from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Brevo API Configuration
    brevo_api_key: str
    brevo_sender_email: EmailStr
    brevo_sender_name: str = "BPO Acceptor"
    
    # Recipients (comma-separated emails in env)
    recipient_emails: str  # Will be parsed into list
    
    # Webhook Security
    webhook_secret: Optional[str] = None
    
    # Application Settings
    app_name: str = "BPO Acceptor Lead Service"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_recipient_list(self) -> List[str]:
        """Parse comma-separated recipient emails into list."""
        return [email.strip() for email in self.recipient_emails.split(",")]


# Create a global settings instance
settings = Settings()

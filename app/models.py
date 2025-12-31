from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class LeadRequest(BaseModel):
    """Lead submission model."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Lead's full name")
    email: EmailStr = Field(..., description="Lead's email address")
    message: str = Field(..., min_length=1, max_length=1000, description="Message from the lead")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "message": "Interested in BPO services"
            }
        }


class LeadResponse(BaseModel):
    """Lead submission response."""
    success: bool
    message: str


class BrevoContactWebhook(BaseModel):
    """Brevo automation webhook payload with contact attributes."""
    
    # Brevo metadata
    appName: Optional[str] = Field(None, description="Brevo app name")
    contact_id: int = Field(..., description="Brevo contact ID")
    email: EmailStr = Field(..., description="Contact email address")
    step_id: int = Field(..., description="Automation step ID")
    workflow_id: int = Field(..., description="Automation workflow ID")
    
    # Contact attributes (nested in 'attributes' object)
    attributes: Dict[str, Any] = Field(..., description="Contact attributes")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "appName": "workflow-action-processor",
                "attributes": {
                    "FIRSTNAME": "John",
                    "MESSAGE": "Interested in BPO services"
                },
                "contact_id": 12345,
                "email": "john@example.com",
                "step_id": 13,
                "workflow_id": 6
            }
        }


class BrevoWebhookEvent(BaseModel):
    """Brevo webhook event model."""
    
    event: str = Field(..., description="Event type (delivered, opened, click, etc.)")
    email: EmailStr = Field(..., description="Recipient email address")
    id: Optional[int] = Field(None, description="Message ID")
    date: Optional[str] = Field(None, description="Event timestamp")
    ts: Optional[int] = Field(None, description="Unix timestamp")
    message_id: Optional[str] = Field(None, alias="message-id", description="Email message ID")
    ts_event: Optional[int] = Field(None, description="Event timestamp")
    subject: Optional[str] = Field(None, description="Email subject")
    tag: Optional[str] = Field(None, description="Email tag")
    sending_ip: Optional[str] = Field(None, description="Sending IP address")
    ts_epoch: Optional[int] = Field(None, description="Epoch timestamp")
    tags: Optional[List[str]] = Field(None, description="Email tags")
    
    # For click events
    link: Optional[str] = Field(None, description="Clicked link URL")
    
    # For bounce/error events
    reason: Optional[str] = Field(None, description="Bounce/error reason")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "event": "delivered",
                "email": "john@example.com",
                "id": 123456,
                "date": "2024-01-01 12:00:00",
                "message-id": "<abc123@domain.com>",
                "subject": "New BPO Lead: John Doe"
            }
        }


class WebhookResponse(BaseModel):
    """Webhook processing response."""
    success: bool
    message: str
    event_type: Optional[str] = None


import logging
from typing import Dict, Any
from app.models import BrevoWebhookEvent
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handler for processing Brevo webhook events."""
    
    def __init__(self):
        self.webhook_secret = settings.WEBHOOK_SECRET
    
    async def process_event(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """
        Process incoming webhook event from Brevo.
        
        Args:
            event: Webhook event data
            
        Returns:
            dict: Processing result
        """
        event_type = event.event
        email = event.email
        
        logger.info(f"Processing webhook event: {event_type} for {email}")
        
        # Route to specific handler based on event type
        handlers = {
            "delivered": self._handle_delivered,
            "opened": self._handle_opened,
            "click": self._handle_click,
            "soft_bounce": self._handle_soft_bounce,
            "hard_bounce": self._handle_hard_bounce,
            "spam": self._handle_spam,
            "blocked": self._handle_blocked,
            "unsubscribed": self._handle_unsubscribed,
            "error": self._handle_error,
        }
        
        handler = handlers.get(event_type, self._handle_unknown)
        return await handler(event)
    
    async def _handle_delivered(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle email delivered event."""
        logger.info(f"✅ Email delivered to {event.email}")
        logger.info(f"   Subject: {event.subject}")
        logger.info(f"   Message ID: {event.message_id}")
        
        # You can add custom logic here:
        # - Update database with delivery status
        # - Trigger analytics tracking
        # - Send notification to admin
        
        return {
            "success": True,
            "message": f"Email delivered to {event.email}",
            "action": "logged"
        }
    
    async def _handle_opened(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle email opened event."""
        logger.info(f"📧 Email opened by {event.email}")
        logger.info(f"   Subject: {event.subject}")
        
        # Custom logic:
        # - Track engagement metrics
        # - Update lead score
        # - Trigger follow-up sequence
        
        return {
            "success": True,
            "message": f"Email opened by {event.email}",
            "action": "engagement_tracked"
        }
    
    async def _handle_click(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle link click event."""
        logger.info(f"🔗 Link clicked by {event.email}")
        logger.info(f"   Link: {event.link}")
        logger.info(f"   Subject: {event.subject}")
        
        # Custom logic:
        # - High engagement indicator
        # - Notify sales team
        # - Update CRM
        # - Send follow-up email
        
        return {
            "success": True,
            "message": f"Link clicked by {event.email}",
            "action": "high_engagement_detected",
            "link": event.link
        }
    
    async def _handle_soft_bounce(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle soft bounce (temporary delivery failure)."""
        logger.warning(f"⚠️ Soft bounce for {event.email}")
        logger.warning(f"   Reason: {event.reason}")
        
        # Custom logic:
        # - Retry sending later
        # - Monitor for pattern
        
        return {
            "success": True,
            "message": f"Soft bounce for {event.email}",
            "action": "retry_scheduled",
            "reason": event.reason
        }
    
    async def _handle_hard_bounce(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle hard bounce (permanent delivery failure)."""
        logger.error(f"❌ Hard bounce for {event.email}")
        logger.error(f"   Reason: {event.reason}")
        
        # Custom logic:
        # - Mark email as invalid in database
        # - Remove from mailing list
        # - Notify admin
        
        return {
            "success": True,
            "message": f"Hard bounce for {event.email}",
            "action": "email_marked_invalid",
            "reason": event.reason
        }
    
    async def _handle_spam(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle spam complaint."""
        logger.warning(f"🚫 Spam complaint from {event.email}")
        
        # Custom logic:
        # - Immediately unsubscribe
        # - Review email content
        # - Update suppression list
        
        return {
            "success": True,
            "message": f"Spam complaint from {event.email}",
            "action": "unsubscribed"
        }
    
    async def _handle_blocked(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle blocked email."""
        logger.warning(f"🛑 Email blocked for {event.email}")
        logger.warning(f"   Reason: {event.reason}")
        
        return {
            "success": True,
            "message": f"Email blocked for {event.email}",
            "action": "logged",
            "reason": event.reason
        }
    
    async def _handle_unsubscribed(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle unsubscribe event."""
        logger.info(f"👋 Unsubscribed: {event.email}")
        
        # Custom logic:
        # - Update database
        # - Remove from active campaigns
        
        return {
            "success": True,
            "message": f"Unsubscribed: {event.email}",
            "action": "removed_from_list"
        }
    
    async def _handle_error(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle error event."""
        logger.error(f"⚠️ Error for {event.email}")
        logger.error(f"   Reason: {event.reason}")
        
        return {
            "success": True,
            "message": f"Error for {event.email}",
            "action": "logged",
            "reason": event.reason
        }
    
    async def _handle_unknown(self, event: BrevoWebhookEvent) -> Dict[str, Any]:
        """Handle unknown event type."""
        logger.warning(f"❓ Unknown event type: {event.event} for {event.email}")
        
        return {
            "success": True,
            "message": f"Unknown event type: {event.event}",
            "action": "logged"
        }


# Create global webhook handler instance
webhook_handler = WebhookHandler()

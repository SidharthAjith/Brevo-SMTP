from fastapi import APIRouter, HTTPException, Request
from app.models import LeadRequest, LeadResponse, BrevoWebhookEvent, WebhookResponse, BrevoContactWebhook
from app.email_service import email_service
from app.webhook_handler import webhook_handler
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/bpo-acceptor-lead", response_model=LeadResponse)
async def submit_lead(lead: LeadRequest):
    """
    Submit a new BPO lead and send notification email.
    
    - **name**: Lead's full name (required)
    - **email**: Lead's email address (required)
    - **message**: Message from the lead (required)
    """
    result = await email_service.send_lead_notification(lead)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return LeadResponse(**result)


# @router.post("/webhook/brevo-contact", response_model=LeadResponse)
# async def brevo_contact_webhook(contact: BrevoContactWebhook):
#     """
#     Receive contact data from Brevo automation and send email notification.
    
#     This endpoint is triggered by Brevo automation when configured to "Call a webhook".
#     Brevo sends contact attributes (EMAIL, NAME, MESSAGE) and this endpoint
#     sends an email notification with that contact information.
    
#     Configure in Brevo:
#     1. Create automation workflow
#     2. Add "Call a webhook" action
#     3. Enable "Include details of the contact who triggered the event"
#     4. Set webhook URL: https://your-domain.com/webhook/brevo-contact
#     5. Ensure contact has EMAIL, NAME, and MESSAGE attributes
    
#     - **EMAIL**: Contact email address (required)
#     - **NAME**: Contact full name (optional, falls back to FNAME)
#     - **MESSAGE**: Contact message (required)
#     """
#     try:
#         logger.info(f"Received contact webhook from Brevo: {contact.EMAIL}")
        
#         # Convert Brevo contact format to LeadRequest format
#         lead = LeadRequest(
#             name=contact.NAME or contact.FNAME or "Unknown",
#             email=contact.EMAIL,
#             message=contact.MESSAGE
#         )
        
#         # Send email notification
#         result = await email_service.send_lead_notification(lead)
        
        
#         if not result["success"]:
#             raise HTTPException(status_code=500, detail=result["message"], data=result)
        
#         logger.info(f"Email sent successfully for contact: {contact.EMAIL}")
#         return LeadResponse(**result)
        
#     except Exception as e:
#         logger.error(f"Error processing Brevo contact webhook: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhook/brevo-contact", response_model=LeadResponse)
async def brevo_contact_webhook(contact: BrevoContactWebhook):
    """
    Receive contact data from Brevo automation and send email notification.
    
    Brevo sends payload with contact attributes in nested 'attributes' object.
    This endpoint extracts FIRSTNAME and MESSAGE, then sends email to configured recipients.
    """
    try:
        logger.info(f"Received contact webhook from Brevo: {contact.email}")
        logger.info(f"Payload: {contact.model_dump()}")
        
        # Extract attributes
        firstname = contact.attributes.get("FIRSTNAME", "")
        lastname = contact.attributes.get("LASTNAME", "")
        message = contact.attributes.get("MESSAGE", "No message provided")
        
        # Convert Brevo contact format to LeadRequest format
        lead = LeadRequest(
            name=firstname or "Unknown",
            email=contact.email,
            message=message
        )
        
        # Send email notification with firstname and lastname
        result = await email_service.send_lead_notification(lead, firstname, lastname)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        
        logger.info(f"Email sent successfully for contact: {contact.email}")
        return LeadResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing Brevo contact webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhook/brevo", response_model=WebhookResponse)
async def brevo_webhook(event: BrevoWebhookEvent, request: Request):
    """
    Receive and process webhook events from Brevo.
    
    This endpoint receives real-time notifications about email events:
    - **delivered**: Email successfully delivered
    - **opened**: Recipient opened the email
    - **click**: Recipient clicked a link
    - **soft_bounce**: Temporary delivery failure
    - **hard_bounce**: Permanent delivery failure
    - **spam**: Marked as spam
    - **unsubscribed**: Recipient unsubscribed
    - **error**: Processing error
    
    Configure this webhook URL in your Brevo dashboard:
    Settings → Webhooks → Add webhook → Enter your domain/webhook/brevo
    """
    try:
        logger.info(f"Received webhook event: {event.event} for {event.email}")
        
        # Process the event
        result = await webhook_handler.process_event(event)
        
        return WebhookResponse(
            success=True,
            message=result.get("message", "Event processed"),
            event_type=event.event
        )
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "BPO Acceptor Lead Service"
    }


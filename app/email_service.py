import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging
from typing import List

from app.config import settings
from app.models import LeadRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Brevo API using official SDK."""
    
    def __init__(self):
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.brevo_api_key
        
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        self.sender_email = settings.brevo_sender_email
        self.sender_name = settings.brevo_sender_name
        self.recipient_emails = settings.get_recipient_list()
    
    async def send_lead_notification(self, lead: LeadRequest, firstname: str = None, lastname: str = None) -> dict:
        """
        Send lead notification email to multiple recipients using Brevo SDK.
        
        Args:
            lead: Lead information
            firstname: Contact's first name (optional)
            lastname: Contact's last name (optional)
            
        Returns:
            dict: Response containing success status and message
        """
        try:
            # Use firstname if provided, otherwise use lead.name
            display_name = firstname if firstname else lead.name
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50; font-size: 24px; margin-bottom: 20px;">Greetings!</h2>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">
                        A new contact has been registered in the BPO <span style="background-color: #c8e6c9; padding: 2px 4px;">Acceptor</span> website. Below are the details:
                    </p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 10px 0; font-size: 16px;"><strong>Name :</strong> {display_name}</p>
                        <p style="margin: 10px 0; font-size: 16px;"><strong>Email Address :</strong> {lead.email}</p>
                        <p style="margin: 10px 0; font-size: 16px;"><strong>Message :</strong> {lead.message}</p>
                    </div>
                    
                    <div style="margin-top: 30px; font-size: 16px;">
                        <p style="margin: 5px 0;">Best Regards,</p>
                        <p style="margin: 5px 0; font-weight: bold;">Rachel Roy</p>
                        <p style="margin: 5px 0;">Business Development Executive</p>
                        <p style="margin: 5px 0;"><a href="http://www.bpoacceptor.com" style="color: #2c3e50; text-decoration: none;">www.bpoacceptor.com</a></p>
                    </div>
                </body>
            </html>
            """
            
            # Prepare sender
            sender = sib_api_v3_sdk.SendSmtpEmailSender(
                name=self.sender_name,
                email=self.sender_email
            )
            
            # Prepare recipients
            to = [sib_api_v3_sdk.SendSmtpEmailTo(email=email) for email in self.recipient_emails]
            
            # Create email object
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                sender=sender,
                to=to,
                subject="New Contact Registration - BPO Acceptor",
                html_content=html_body
            )
            
            # Send email
            logger.info(f"Sending lead notification to {len(self.recipient_emails)} recipients via Brevo SDK")
            
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            
            logger.info("Lead notification sent successfully via Brevo SDK")
            logger.info(f"Brevo message ID: {api_response.message_id}")
            
            return {
                "success": True,
                "message": "Lead submitted successfully"
            }
            
        except ApiException as e:
            logger.error(f"Brevo API error: {e}")
            return {
                "success": False,
                "message": f"Failed to send notification: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "message": f"Error processing lead: {str(e)}"
            }


# Create a global email service instance
email_service = EmailService()

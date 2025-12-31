import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging

from app.config import settings
from app.models import LeadRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Brevo SMTP."""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.from_name = settings.smtp_from_name
        self.recipient_email = settings.recipient_email
    
    async def send_lead_notification(self, lead: LeadRequest) -> dict:
        """
        Send lead notification email.
        
        Args:
            lead: Lead information
            
        Returns:
            dict: Response containing success status and message
        """
        try:
            # Create email subject
            subject = f"New BPO Lead: {lead.name}"
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #2c3e50;">New Lead Submission</h2>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <p><strong>Name:</strong> {lead.name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{lead.email}">{lead.email}</a></p>
                        <p><strong>Message:</strong></p>
                        <p style="background-color: white; padding: 10px; border-left: 3px solid #3498db;">{lead.message}</p>
                    </div>
                    <p style="margin-top: 20px; color: #7f8c8d; font-size: 12px;">
                        This email was sent from the BPO Acceptor Lead Service.
                    </p>
                </body>
            </html>
            """
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = formataddr((self.from_name, self.from_email))
            message["To"] = self.recipient_email
            
            # Add HTML body
            message.attach(MIMEText(html_body, "html"))
            
            # Send email
            logger.info(f"Sending lead notification to {self.recipient_email}")
            
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=False,
                start_tls=True
            ) as smtp:
                await smtp.login(self.smtp_username, self.smtp_password)
                await smtp.send_message(message)
                
            logger.info("Lead notification sent successfully")
            
            return {
                "success": True,
                "message": "Lead submitted successfully"
            }
            
        except aiosmtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
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

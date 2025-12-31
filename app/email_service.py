import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging
from typing import List

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
        self.recipient_emails = settings.get_recipient_list()
    
    async def send_lead_notification(self, lead: LeadRequest, firstname: str = None, lastname: str = None) -> dict:
        """
        Send lead notification email to multiple recipients.
        
        Args:
            lead: Lead information
            firstname: Contact's first name (optional)
            lastname: Contact's last name (optional)
            
        Returns:
            dict: Response containing success status and message
        """
        try:
            # Create email subject
            subject = "New Contact Registration - BPO Acceptor"
            
            # Use firstname if provided, otherwise use lead.name
            display_name = firstname if firstname else lead.name
            
            # Create HTML email body matching the template
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
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = formataddr((self.from_name, self.from_email))
            message["To"] = ", ".join(self.recipient_emails)
            
            # Add HTML body
            message.attach(MIMEText(html_body, "html"))
            
            # Send email
            logger.info(f"Sending lead notification to {len(self.recipient_emails)} recipients")
            logger.info(f"Connecting to {self.smtp_host}:{self.smtp_port}")
            
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=False,
                start_tls=True,
                timeout=30  # 30 second timeout
            ) as smtp:
                logger.info("SMTP connection established, logging in...")
                await smtp.login(self.smtp_username, self.smtp_password)
                logger.info("Login successful, sending message...")
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

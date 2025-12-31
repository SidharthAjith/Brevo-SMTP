import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_smtp():
    """Test SMTP connection to Brevo."""
    
    smtp_host = os.getenv("SMTP_HOST", "smtp-relay.brevo.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL")
    
    print(f"Testing SMTP connection...")
    print(f"Host: {smtp_host}")
    print(f"Port: {smtp_port}")
    print(f"Username: {smtp_username}")
    print(f"From Email: {smtp_from_email}")
    print("-" * 50)
    
    try:
        print("Attempting to connect...")
        async with aiosmtplib.SMTP(
            hostname=smtp_host,
            port=smtp_port,
            use_tls=False,
            start_tls=True,
            timeout=30
        ) as smtp:
            print("✅ Connection established!")
            
            print("Attempting to login...")
            await smtp.login(smtp_username, smtp_password)
            print("✅ Login successful!")
            
            print("\n🎉 SMTP connection test PASSED!")
            print("Your SMTP credentials are correct and the connection works.")
            
    except asyncio.TimeoutError:
        print("❌ Connection timed out!")
        print("\nPossible causes:")
        print("1. Firewall blocking port 587")
        print("2. Network restrictions (corporate network, VPN, etc.)")
        print("3. ISP blocking SMTP ports")
        print("\nSolutions:")
        print("- Try from a different network (mobile hotspot)")
        print("- Check Windows Firewall settings")
        print("- Contact your network administrator")
        
    except aiosmtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\nCheck your SMTP credentials:")
        print("- SMTP_USERNAME should be your Brevo login email")
        print("- SMTP_PASSWORD should be your Brevo SMTP key (not account password)")
        print("- Get SMTP key from: Brevo → Settings → SMTP & API")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_smtp())

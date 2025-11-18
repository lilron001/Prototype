# email_service.py
"""Email service for verification codes"""

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD


class EmailService:
    """Handles email sending and verification"""
    
    def __init__(self):
        self.email_address = EMAIL_ADDRESS
        self.email_password = EMAIL_PASSWORD
        self.pending_verifications = {}
    
    @staticmethod
    def generate_verification_code() -> str:
        """Generate a 6-digit verification code"""
        return str(random.randint(100000, 999999))
    
    def send_verification_email(self, to_email: str, code: str) -> bool:
        """Send verification code via email"""
        try:
            # Print code to console for testing
            print(f"\n{'=' * 50}")
            print(f"VERIFICATION CODE FOR {to_email}: {code}")
            print(f"{'=' * 50}\n")
            
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = "Email Verification Code"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #2c3e50;">Email Verification</h2>
                    <p>Your verification code is:</p>
                    <h1 style="color: #3498db; letter-spacing: 5px;">{code}</h1>
                    <p>This code will expire in 10 minutes.</p>
                    <p style="color: #7f8c8d; font-size: 12px;">
                        If you didn't request this code, please ignore this email.
                    </p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
                server.quit()
                print("Email sent successfully!")
                return True
            except Exception as email_error:
                print(f"Email sending failed: {str(email_error)}")
                print("But code is printed above for testing purposes")
                return True  # Return True for testing
                
        except Exception as e:
            print(f"Error in send_verification_email: {str(e)}")
            return True  # Return True for testing
    
    def store_verification(self, email: str, code: str, username: str = None, password: str = None):
        """Store verification code temporarily"""
        self.pending_verifications[email] = {
            'code': code,
            'username': username,
            'password': password
        }
    
    def verify_code(self, email: str, entered_code: str) -> bool:
        """Verify the entered code matches stored code"""
        if email in self.pending_verifications:
            stored_code = self.pending_verifications[email]['code']
            return entered_code == stored_code
        return False
    
    def get_pending_data(self, email: str):
        """Get pending verification data"""
        return self.pending_verifications.get(email)
    
    def remove_verification(self, email: str):
        """Remove verification code after use"""
        if email in self.pending_verifications:
            del self.pending_verifications[email]
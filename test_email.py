import smtplib
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ---> UPDATE THIS TO YOUR EMAIL <---
TEST_RECEIVER = "manavchawla03@gmail.com" 

print(f"Attempting to log into Gmail as: {SENDER_EMAIL}")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    print("❌ ERROR: Could not find email or password in your .env file!")
    exit()

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # This turns on "Debug Mode" to print the exact conversation with Google
        server.set_debuglevel(1) 
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send a basic text email
        message = f"Subject: Python Test\n\nIf you are reading this, your credentials work perfectly."
        server.sendmail(SENDER_EMAIL, TEST_RECEIVER, message)
        
    print("\n✅ EMAIL SENT SUCCESSFULLY! Check your inbox.")
except smtplib.SMTPAuthenticationError:
    print("\n❌ AUTHENTICATION ERROR: Google rejected your password. Ensure you are using a 16-character 'App Password', NOT your normal Gmail password.")
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
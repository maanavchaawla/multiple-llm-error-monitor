import pandas as pd
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# LLM Providers
from google import genai
from groq import Groq
from openai import OpenAI

# Background Monitoring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================================
# 1. Configuration & Setup
# ==========================================
load_dotenv()
GEMINI_KEY = os.getenv("LLM_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Safely load and split emails from the .env file
to_env = os.getenv("TO_EMAILS", "manavchawla03@gmail.com")
cc_env = os.getenv("CC_EMAILS", "")

# Convert comma-separated strings into neat Python lists
STAKEHOLDER_TO = [email.strip() for email in to_env.split(",") if email.strip()]
STAKEHOLDER_CC = [email.strip() for email in cc_env.split(",") if email.strip()]

EXCEL_FILE_NAME = "error_logs.xlsx"
EXCEL_FILE_PATH = os.path.abspath(EXCEL_FILE_NAME)

# Initialize Clients safely
client_gemini = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
client_groq = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
client_openai = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

# Fallback Strategy
FALLBACK_STRATEGY = [
    {'provider': 'google', 'model': 'gemini-2.5-flash'},
    {'provider': 'groq', 'model': 'llama-3.1-8b-instant'},
    {'provider': 'openai', 'model': 'gpt-4o-mini'}
]

# ==========================================
# 2. Core Functions
# ==========================================
def wait_for_file_unlock(filepath, timeout=5):
    """Prevents crashes by waiting if the user currently has Excel open."""
    if not os.path.exists(filepath):
        print(f"   [FILE ERROR] Cannot find {filepath}")
        return False
        
    start_time = time.time()
    while True:
        try:
            # Rename trick checks if the file is locked by the OS
            os.rename(filepath, filepath)
            return True
        except OSError:
            if time.time() - start_time > timeout:
                print("   [FILE LOCKED] Microsoft Excel has the file open. You MUST close the Excel window!")
                return False
            time.sleep(1)

def analyze_error(error_type, description):
    """Cycles through LLMs until one provides an answer."""
    prompt = f"Analyze error: {error_type}. Description: {description}. Provide a 2-sentence summary and a short resolution in HTML format. Use <b> and <br>."
    
    for attempt in FALLBACK_STRATEGY:
        provider = attempt['provider']
        model_name = attempt['model']
        print(f"   -> Asking [ {provider.upper()}: {model_name} ]...")
        
        try:
            if provider == 'google' and client_gemini:
                response = client_gemini.models.generate_content(model=model_name, contents=prompt)
                return response.text
            elif provider == 'groq' and client_groq:
                response = client_groq.chat.completions.create(
                    model=model_name, messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            elif provider == 'openai' and client_openai:
                response = client_openai.chat.completions.create(
                    model=model_name, messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
        except Exception as e:
            print(f"   [API FAILED] {provider} error: {str(e)[:40]}")
            time.sleep(1)
            
    return "<b>LLM Analysis Failed.</b><br>All API providers are down."

def send_email(error_id, error_type, llm_response):
    """Formats and sends the email to explicitly defined TO and CC envelopes."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("   [EMAIL FAILED] Missing Email Credentials in .env file!")
        return False

    if not STAKEHOLDER_TO:
        print("   [EMAIL FAILED] No 'TO_EMAILS' defined in .env file!")
        return False

    # 1. Build the visible headers
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(STAKEHOLDER_TO)
    
    if STAKEHOLDER_CC:
        msg['Cc'] = ", ".join(STAKEHOLDER_CC)
        
    msg['Subject'] = f"System Alert: {error_type} ({error_id})"
    
    body = f"<h2>Error: {error_id}</h2><p>Type: {error_type}</p><hr><h3>AI Resolution</h3>{llm_response}"
    msg.attach(MIMEText(body, 'html'))

    # 2. Create the explicit envelope list for the SMTP server
    all_recipients = STAKEHOLDER_TO + STAKEHOLDER_CC

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            # Use sendmail to force delivery to every address in the combined list
            server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
            
        print(f"   [EMAIL SUCCESS] Sent alert for {error_id} (Delivered to TO and CC lists)")
        return True
    except smtplib.SMTPAuthenticationError:
        print("   [EMAIL FAILED] Authentication Error. Check App Password.")
        return False
    except Exception as e:
        print(f"   [EMAIL FAILED] Critical Network Error: {e}")
        return False

def process_excel():
    """Reads Excel and processes pending errors."""
    if not wait_for_file_unlock(EXCEL_FILE_PATH):
        return

    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
    except Exception:
        return 

    pending = df[df['Status'].astype(str).str.strip().str.title() == 'Pending']
    if pending.empty:
        return

    for index, row in pending.iterrows():
        print(f"\n[NEW ERROR DETECTED] Processing {row['Error_ID']}...")
        llm_response = analyze_error(row['Error_Type'], row['Description'])
        
        if send_email(row['Error_ID'], row['Error_Type'], llm_response):
            df.at[index, 'Status'] = 'Processed'
    
    if wait_for_file_unlock(EXCEL_FILE_PATH):
        df.to_excel(EXCEL_FILE_PATH, index=False)
        print("   [DATABASE UPDATED] Excel saved.")

# ==========================================
# 3. Watchdog Event Handler
# ==========================================
class ExcelMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(EXCEL_FILE_NAME):
            time.sleep(1.5) # Wait for OS to finish writing
            process_excel()

if __name__ == "__main__":
    print("==================================================")
    print(" Background Event Monitor Started...              ")
    print(" Email CC Routing: ENABLED (Explicit Envelope)    ")
    print(" Waiting silently for Excel modifications...      ")
    print("==================================================")
    
    process_excel()
    
    current_directory = os.path.dirname(EXCEL_FILE_PATH) or "."
    event_handler = ExcelMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=current_directory, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
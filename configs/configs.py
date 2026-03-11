import os
from dotenv import load_dotenv

# Load environment variables from a .env file (This is how Docker will pass secrets)
load_dotenv()

# Build relative paths dynamically based on the project's root directory
# This ensures it works on your laptop, your coworker's VM, and inside Docker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# We will tell your coworker to put their files inside a 'data' folder in the project
BANK_STATEMENT_PATH = os.path.join(BASE_DIR, "data", "CustomMatchingbank.xlsx")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "data", "screenshots")

# -----------------------------------------
# ENVIRONMENT VARIABLES (Database & API)
# -----------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "transfer_reconciliation")

# -----------------------------------------
# PROMPTS
# -----------------------------------------
LLM_PROMPT = """
You are an expert financial data extractor. Your task is to extract information from a bank transfer screenshot text.

EXTRACT THE FOLLOWING FIELDS:
1. Amount Transferred: The net amount sent (strictly EXCLUDE any bank/transfer fees).
2. Fee Amount: The specific cost of the transaction fee, if listed. If not listed, return "0".
3. Sender/Receiver Name: The full name identified in the transaction.
4. Email: Any email address associated with the transaction.
5. Mobile Number: Any Egyptian mobile number (usually starting with 010, 011, 012, or 015). 
   *CRITICAL RULE:* If the transfer uses an email/username (like Instapay) and no mobile number is explicitly written in the text, you MUST return "null". Do not guess or hallucinate a phone number.
6. Transaction Reference: The unique ID, Ref Number, or Transaction ID.
7. Transaction Date: The date and time the transfer occurred.

OUTPUT RULES:
- Output the result strictly in valid JSON format.
- Use "null" for any field that is not found in the text.
- Do not provide any conversational filler or explanation.

The following is the text extracted via OCR:
"""
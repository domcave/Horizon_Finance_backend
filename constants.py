import os

from dotenv import load_dotenv

load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET_KEY = os.getenv("PLAID_SECRET_KEY")

openai_secret_key = os.getenv("OPENAI_API_KEY")
openai_assistant_id = os.getenv("OPENAI_ASSISTANT_ID")


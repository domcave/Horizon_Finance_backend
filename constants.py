import os

from dotenv import load_dotenv

load_dotenv()

openai_secret_key = os.getenv("OPENAI_API_KEY")
openai_assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
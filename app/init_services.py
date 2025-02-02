from app.services.auth_service import AuthService
from app.services.openai_service import OpenAIService
from app.services.plaid_service import PlaidService

auth_service = AuthService()    
ai_service = OpenAIService()
plaid_service = PlaidService()

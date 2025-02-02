from app.services.auth_service import AuthService
from app.services.openai_service import OpenAIService
from app.services.plaid_service import PlaidService
from app.services.house_recommendation_service import HouseRecommendation
from app.services.marriage_recommendation_service import MarriageRecommendation
from app.services.retirement_recommendation_service import RetirementRecommendation

auth_service = AuthService()    
ai_service = OpenAIService()
plaid_service = PlaidService()
house_rec_service = HouseRecommendation()
marraige_rec_service = MarriageRecommendation()
retirement_rec_service = RetirementRecommendation()

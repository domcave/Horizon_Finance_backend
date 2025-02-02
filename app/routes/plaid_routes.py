from flask import Blueprint, request, jsonify
import plaid
from plaid.api import plaid_api
import plaid.apis
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import json
from app.models.user import User
import constants
from flask_cors import CORS
import datetime
from app.init_services import plaid_service
from app.extensions import db

plaid_bp = Blueprint('plaid', __name__)
CORS(plaid_bp)

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': constants.PLAID_CLIENT_ID,
        'secret': constants.PLAID_SECRET_KEY,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def getUserAccessToken(username):
        ACCESS_TOKEN = db.session.query(User).filter(User.username == username).first().access_token
        return ACCESS_TOKEN


@plaid_bp.route("/link_token", methods=["POST"])
def generateLinkToken():
    data = request.get_json()
    user_id = data.get("user_id")
    
    if not user_id or not isinstance(user_id, str):
        print("Invalid user_id")
        return jsonify({"error": "Invalid user_id, expected a non-empty string"}), 400

    request_data = LinkTokenCreateRequest(
        client_name='Horizon Finance',
        language='en',
        country_codes=[CountryCode("US")],
        user=LinkTokenCreateRequestUser(client_user_id=user_id),  
        products=[
            Products("auth"), 
            Products("transactions"),
            Products("investments"), 
            Products("liabilities")
        ],
    )
    try:
        response = client.link_token_create(request_data).to_dict()
        link_token = response['link_token']
        print(link_token)
        response = jsonify(response)
        print('link_token')
        return response, 200
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error creating Link token: {error_message}")
        return jsonify({"error": error_message}), 400

@plaid_bp.route("/access_token", methods=["POST"])
def exchangePublicForAccess():
    data = request.get_json()
    username = data.get("username")
    pub_token = data.get("public_token")
    if not pub_token:
        return jsonify({"error": "Missing public_token"}), 400

    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=pub_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        ACCESS_TOKEN = exchange_response.to_dict()['access_token']
        # Save access token to DB
        user = db.session.query(User).filter(User.username == username).first()
        user.access_token = ACCESS_TOKEN
        db.session.commit()
        return jsonify({ "access_token": ACCESS_TOKEN }), 200
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error exchanging token: {error_message}")
        return jsonify({"error": error_message}), 400
        

@plaid_bp.route("/transactions/30days", methods=["GET"])
def getTransactionsLast30():
    username = request.args.get("username")  # Extracts username from query params
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=30)
    
    ACCESS_TOKEN = getUserAccessToken(username)

    
    body = {
        "access_token": ACCESS_TOKEN,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
    }
    try:
        response = client.transactions_get(body).to_dict()
        transactions = plaid_service.processTransactions(response)
        return jsonify(transactions), 200
        
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error getting transactions: {error_message}")
        return jsonify({"error": error_message}), 400
    
    
@plaid_bp.route("/transactions/month", methods=["GET"])
def getTransactionsThisMonth():
    username = request.args.get("username")  # Extracts username from query params
    end = datetime.datetime.now()
    start = end.replace(day=1)  # First day of the current month
    
    ACCESS_TOKEN = getUserAccessToken(username)
    
    body = {
        "access_token": ACCESS_TOKEN,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
    }
    try:
        response = client.transactions_get(body).to_dict()
        transactions = plaid_service.processTransactions(response)
        return jsonify(transactions), 200
        
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error getting transactions: {error_message}")
        return jsonify({"error": error_message}), 400
    
    
@plaid_bp.route("/investments/holdings", methods=["GET"])
def getInvestmentHoldings():
    username = request.args.get("username")  # Extracts username from query params
    ACCESS_TOKEN = getUserAccessToken(username)
    body = {
        "access_token": ACCESS_TOKEN
    }
    try:
        response = client.investments_holdings_get(body).to_dict()
        investments = plaid_service.processInvestments(response)
        return jsonify(investments), 200
        
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error getting investments: {error_message}")
        return jsonify({"error": error_message}), 400
        
        
        
@plaid_bp.route("/accounts/balance", methods=["GET"])
def getAccountBalances():
    username = request.args.get("username")  # Extracts username from query params
    ACCESS_TOKEN = getUserAccessToken(username)
    body = {
        "access_token": ACCESS_TOKEN
    }
    try:
        response = client.accounts_balance_get(body).to_dict()
        investments = plaid_service.processAccountBalances(response)
        return jsonify(investments), 200
        
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error getting account balances: {error_message}")
        return jsonify({"error": error_message}), 400
        
    

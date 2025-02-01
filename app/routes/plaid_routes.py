from flask import Blueprint, request, jsonify
import plaid
from plaid.api import plaid_api
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import json
import constants
from flask_cors import CORS

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

@plaid_bp.route("/link_token", methods=["POST"])
def generateLinkToken():
    data = request.get_json()
    user_id = data.get("user_id")
    
    # Validate user_id
    if not user_id or not isinstance(user_id, str):
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
    pub_token = data.get("public_token")
    if not pub_token:
        return jsonify({"error": "Missing public_token"}), 400

    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=pub_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response.to_dict()['access_token']
        # Save access token to DB
        return jsonify({ "access_token": access_token }), 200
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error exchanging token: {error_message}")
        return jsonify({"error": error_message}), 400
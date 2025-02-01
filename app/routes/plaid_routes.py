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

plaid_bp = Blueprint('plaid', __name__)

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
    request_data = LinkTokenCreateRequest(
        client_name='Horizon Finance',
        language='en',
        country_codes=[CountryCode("US")],
        user=LinkTokenCreateRequestUser(client_user_id='user'),  # Replace with actual user ID
        products=[
            Products("auth"), 
            Products("transactions"),
            Products("investments"), 
            Products("liabilities")
        ],
    )
    try:
        response = client.link_token_create(request_data)
        link_token = response.to_dict()['link_token']
        print(link_token)
        return jsonify(response.to_dict()), 200
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
        return jsonify({"access_token": access_token}), 200
    except plaid.ApiException as e:
        error_message = json.loads(e.body)
        print(f"Error exchanging token: {error_message}")
        return jsonify({"error": error_message}), 400
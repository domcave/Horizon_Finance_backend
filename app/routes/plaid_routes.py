from flask import Blueprint, request, jsonify
import plaid
from plaid.api import plaid_api
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import json

plaid_bp = Blueprint('plaid', __name__)

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': constant,
        'secret': secret,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@plaid_bp.route("/accesstoken", methods=["POST"])
def exchangePublicForAccess():
    data = request.get_json()
    
    # the public token is received from Plaid Link
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=pt_response['public_token']
    )
    exchange_response = client.item_public_token_exchange(exchange_request)
    access_token = exchange_response['access_token']


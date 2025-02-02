import datetime

class PlaidService:
    
    def processTransactions(self, transactions: dict):
        processed_data = {
            "total_transactions": transactions.get("total_transactions", 0),
            "error": transactions.get("item", {}).get("error"),
            "transactions": []
        }

        for txn in transactions.get("transactions", []):
            processed_data["transactions"].append({
                "account_id": txn.get("account_id"),
                "amount": txn.get("amount"),
                "category": txn.get("category", [None])[0],  # First category
                "category_id": txn.get("category_id"),
                "date": txn.get("date"),
                "datetime": txn.get("datetime"),
                "name": txn.get("name"),
                "merchant_name": txn.get("merchant_name"),
                "payment_channel": txn.get("payment_channel"),
            })

        return processed_data
    
    
    def processInvestments(self, investments: dict):
        accounts = investments.get("accounts", [])
        holdings = investments.get("holdings", [])
        securities = {sec["security_id"]: sec for sec in investments.get("securities", [])}

        # Total balance per account
        account_balances = {
            acc["account_id"]: {
                "name": acc["name"],
                "balance": acc["balances"].get("current", 0)
            }
            for acc in accounts
        }

        # Holdings breakdown by security
        holdings_by_security = {}

        for holding in holdings:
            security_id = holding["security_id"]
            value = holding.get("institution_value", 0)

            if security_id not in holdings_by_security:
                sec = securities.get(security_id, {})
                holdings_by_security[security_id] = {
                    "security_name": sec.get("name", "Unknown"),
                    "ticker": sec.get("ticker_symbol", None),
                    "type": sec.get("type", None),
                    "close_price": sec.get("close_price", None),
                    "close_price_as_of": sec.get("close_price_as_of", None),
                    "sector": sec.get("sector", None),
                    "option_contract": sec.get("option_contract", None),
                    "total_value": 0
                }
            holdings_by_security[security_id]["total_value"] += value

        return {
            "account_balances": account_balances,
            "holdings_by_security": holdings_by_security
        }
        
    def processAccountBalances(self, balances: dict):
        # Extracting account data
        accounts = balances.get("accounts", [])
        account_data = {}

        for account in accounts:
            account_id = account.get("account_id")
            available = account.get("balances", {}).get("available")
            current = account.get("balances", {}).get("current")
            iso_currency_code = account.get("balances", {}).get("iso_currency_code")
            account_type = account.get("type")
            account_subtype = account.get("subtype")
            
            # Assuming we don't have a specific "last updated" field, adding a placeholder
            last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            account_data[account_id] = {
                "available": available,
                "current": current,
                "last_updated": last_updated,
                "account_type": account_type,
                "account_subtype": account_subtype,
                "currency_code": iso_currency_code
            }

        # Extracting error information, if present
        error = balances.get("item", {}).get("error", None)

        return {
            "accounts": account_data,
            "error": error
        }
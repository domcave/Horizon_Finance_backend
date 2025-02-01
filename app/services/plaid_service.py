import datetime

class PlaidService:
    
    def processTransactions(transactions: dict):
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


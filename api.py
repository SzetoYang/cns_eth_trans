from fastapi import FastAPI, HTTPException
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
ETHERSCAN_API_URL = os.getenv("ETHERSCAN_API_URL", "https://api.etherscan.io/v2/api")


def parse_etherscan_tx(tx_data, wallet_address):
    current_time = int(time.time())
    result = {}
    result["tx_hash"] = tx_data["hash"]
    result["method"] = (
        "Contract Interaction" if tx_data["input"] != "0x" else "Transfer"
    )
    if tx_data["to"].lower() == "0xdac17f958d2ee523a2206206994597c13d831ec7":
        result["method"] = "Transfer (USDT)"
    result["block"] = int(tx_data["blockNumber"])
    tx_time = int(tx_data["timeStamp"])
    age_seconds = current_time - tx_time
    result["days_age"] = f"{age_seconds // (24 * 3600)} days ago"
    result["age"] = tx_time
    result["from"] = tx_data["from"]
    result["to"] = tx_data["to"]
    result["amount"] = (
        f"{int(tx_data['value']) / 10**18} ETH"
        if int(tx_data["value"]) > 0
        else "0 ETH"
    )
    fee = int(tx_data["gasUsed"]) * int(tx_data["gasPrice"]) / 10**18
    result["txnfee"] = f"{fee:.6f} ETH"
    wallet_address = wallet_address.lower()
    result["type"] = (
        "Sell"
        if result["from"].lower() == wallet_address
        else "Buy" if result["to"].lower() == wallet_address else "N/A"
    )
    return result


@app.get("/transactions/{address}")
async def get_transactions(
    address: str, startblock: int = 0, endblock: int = 99999999, sort: str = "desc"
):
    if not API_KEY:
        raise HTTPException(
            status_code=500, detail="Etherscan API Key is not configured"
        )

    params = {
        "chainid": 1,
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": startblock,
        "endblock": endblock,
        "sort": sort,
        "apikey": API_KEY,
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "1":
            raise HTTPException(
                status_code=400, detail=data.get("message", "API error")
            )
        transactions = data["result"]
        parsed_txs = [parse_etherscan_tx(tx, address) for tx in transactions]
        return {"status": "success", "address": address, "transactions": parsed_txs}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

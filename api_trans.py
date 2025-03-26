from fastapi import FastAPI, HTTPException
import aiohttp
import asyncio
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
        "Sell" if result["from"].lower() == wallet_address
        else "Buy" if result["to"].lower() == wallet_address else "N/A"
    )
    return result

def parse_token_tx(tx_data, wallet_address):
    current_time = int(time.time())
    result = {}
    result["tx_hash"] = tx_data["hash"]
    result["block"] = int(tx_data["blockNumber"])
    tx_time = int(tx_data["timeStamp"])
    age_seconds = current_time - tx_time
    result["days_age"] = f"{age_seconds // (24 * 3600)} days ago"
    result["age"] = tx_time
    result["from"] = tx_data["from"]
    result["to"] = tx_data["to"]
    result["contractAddress"] = tx_data["contractAddress"]
    result["tokenName"] = tx_data["tokenName"]
    result["tokenSymbol"] = tx_data["tokenSymbol"]
    result["value"] = f"{int(tx_data['value']) / 10**int(tx_data['tokenDecimal'])} {tx_data['tokenSymbol']}"
    wallet_address = wallet_address.lower()
    result["type"] = (
        "Sell" if result["from"].lower() == wallet_address
        else "Buy" if result["to"].lower() == wallet_address else "N/A"
    )
    return result

def parse_nft_tx(tx_data, wallet_address):
    current_time = int(time.time())
    result = {}
    result["tx_hash"] = tx_data["hash"]
    result["block"] = int(tx_data["blockNumber"])
    tx_time = int(tx_data["timeStamp"])
    age_seconds = current_time - tx_time
    result["days_age"] = f"{age_seconds // (24 * 3600)} days ago"
    result["age"] = tx_time
    result["from"] = tx_data["from"]
    result["to"] = tx_data["to"]
    result["contractAddress"] = tx_data["contractAddress"]
    result["tokenName"] = tx_data["tokenName"]
    result["tokenSymbol"] = tx_data["tokenSymbol"]
    result["tokenID"] = tx_data["tokenID"]
    wallet_address = wallet_address.lower()
    result["type"] = (
        "Sell" if result["from"].lower() == wallet_address
        else "Buy" if result["to"].lower() == wallet_address else "N/A"
    )
    return result

def parse_erc1155_tx(tx_data, wallet_address):
    current_time = int(time.time())
    result = {}
    result["tx_hash"] = tx_data["hash"]
    result["block"] = int(tx_data["blockNumber"])
    tx_time = int(tx_data["timeStamp"])
    age_seconds = current_time - tx_time
    result["days_age"] = f"{age_seconds // (24 * 3600)} days ago"
    result["age"] = tx_time
    result["from"] = tx_data["from"]
    result["to"] = tx_data["to"]
    result["contractAddress"] = tx_data["contractAddress"]
    result["tokenName"] = tx_data["tokenName"]
    result["tokenSymbol"] = tx_data["tokenSymbol"]
    result["tokenID"] = tx_data["tokenID"]
    result["tokenValue"] = tx_data["tokenValue"]
    wallet_address = wallet_address.lower()
    result["type"] = (
        "Sell" if result["from"].lower() == wallet_address
        else "Buy" if result["to"].lower() == wallet_address else "N/A"
    )
    return result

async def fetch_etherscan_data(session, params):
    try:
        async with session.get(ETHERSCAN_API_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            print(f"API Response for {params['action']}: {data}")
            if data.get("status") not in ["1", "0"]:
                raise HTTPException(
                    status_code=400, detail=data.get("message", "API error")
                )
            return data["result"] if data.get("status") == "1" else []
    except aiohttp.ClientError as e:
        print(f"Request failed for {params['action']}: {str(e)}")
        return []

@app.get("/transactions/{address}")
async def get_all_transactions(
    address: str, startblock: int = 0, endblock: int = 99999999, sort: str = "desc"
):
    if not API_KEY:
        raise HTTPException(
            status_code=500, detail="Etherscan API Key is not configured"
        )

    base_params = {
        "chainid": 1,
        "module": "account",
        "address": address,
        "startblock": startblock,
        "endblock": endblock,
        "sort": sort,
        "apikey": API_KEY,
    }

    result = {"status": "success", "address": address, "transactions": {}}

    async with aiohttp.ClientSession() as session:
        try:
            normal_params = base_params.copy()
            normal_params["action"] = "txlist"
            token_params = base_params.copy()
            token_params["action"] = "tokentx"
            nft_params = base_params.copy()
            nft_params["action"] = "tokennfttx"
            erc1155_params = base_params.copy()
            erc1155_params["action"] = "token1155tx"

            normal_task = fetch_etherscan_data(session, normal_params)
            token_task = fetch_etherscan_data(session, token_params)
            nft_task = fetch_etherscan_data(session, nft_params)
            erc1155_task = fetch_etherscan_data(session, erc1155_params)

            normal_txs, token_txs, nft_txs, erc1155_txs = await asyncio.gather(
                normal_task, token_task, nft_task, erc1155_task, return_exceptions=True
            )

            result["transactions"]["normal_txs"] = (
                [parse_etherscan_tx(tx, address) for tx in normal_txs]
                if isinstance(normal_txs, list) else []
            )
            result["transactions"]["token_txs"] = (
                [parse_token_tx(tx, address) for tx in token_txs]
                if isinstance(token_txs, list) else []
            )
            result["transactions"]["nft_txs"] = (
                [parse_nft_tx(tx, address) for tx in nft_txs]
                if isinstance(nft_txs, list) else []
            )
            result["transactions"]["erc1155_txs"] = (
                [parse_erc1155_tx(tx, address) for tx in erc1155_txs]
                if isinstance(erc1155_txs, list) else []
            )

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

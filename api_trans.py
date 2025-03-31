from fastapi import FastAPI, HTTPException
import aiohttp
import asyncio
from meta import *
from dotenv import load_dotenv
import os
from aiohttp_socks import ProxyConnector

load_dotenv()

app = FastAPI()


async def fetch_etherscan_data(session, api_url, headers, params, chain="eth"):
    try:
        async with session.get(api_url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            if chain != "tron":
                if data.get("status") not in ["1", "0"]:
                    raise HTTPException(
                        status_code=400, detail=data.get("message", "API error")
                    )
                return data["result"] if data.get("status") == "1" else []
            else:
                return data.get("data", [])
    except aiohttp.ClientError as e:
        print(f"Request failed for {params.get('action', 'tron')} on {api_url}: {str(e)}")
        return []


@app.get("/transactions/{chain}/{address}")
async def get_all_transactions(
        chain: str,
        address: str,
):
    if chain not in URL_META.keys():
        raise HTTPException(status_code=400,
                            detail=f"Unsupported chain: {chain}. Use {' '.join(URL_META.keys()[:-1])} or {URL_META.keys()[-1]}.")

    api_url = os.getenv(URL_META[chain])
    api_key = os.getenv(KEY_META[chain])

    if not api_key:
        raise HTTPException(
            status_code=500, detail=f"{chain.upper()} API Key is not configured"
        )

    result = {"status": "success", "chain": chain, "address": address, "transactions": {}}

    connector = ProxyConnector.from_url('socks5://10.0.0.1:10080')
    async with aiohttp.ClientSession(connector=connector) as session:
    # async with aiohttp.ClientSession() as session:
        try:
            tasks = []
            task_mapping = []
            for tx_type in API_META[chain].keys():
                meta = API_META[chain][tx_type].copy()
                url = api_url + meta['api_prefix']
                api_key_meta = meta['api_key']
                address_meta = meta['address']
                meta[api_key_meta[0]].update({api_key_meta[1]: api_key})
                for each_address_meta in address_meta:
                    headers = meta['headers'].copy()
                    params = meta['params'].copy()
                    params.update({each_address_meta[1]: address})
                    tasks.append(fetch_etherscan_data(session, url, headers, params, chain))
                    task_mapping.append(tx_type)

            data = await asyncio.gather(*tasks, return_exceptions=True)

            for tx_type, tx_data in zip(task_mapping, data):
                if not isinstance(tx_data, Exception):
                    if tx_type not in result["transactions"]:
                        result["transactions"][tx_type + '_txs'] = []
                    meta = API_META[chain][tx_type]
                    format_result = meta.get("format_result", True)  # 默认 True
                    if format_result:
                        results_meta = meta["results"]
                        formatted_data = []
                        for tx in tx_data:
                            formatted_tx = {}
                            for key, rule in results_meta.items():
                                try:
                                    if rule.__code__.co_argcount == 2:
                                        formatted_tx[key] = rule(tx, address.lower())
                                    else:
                                        formatted_tx[key] = rule(tx)
                                except Exception as e:
                                    formatted_tx[key] = f"Error: {str(e)}"
                            formatted_data.append(formatted_tx)
                        result["transactions"][tx_type + '_txs'].extend(formatted_data)
                    else:
                        result["transactions"][tx_type + '_txs'].extend(tx_data)

            if format_result:
                for tx_type in result["transactions"]:
                    seen_hashes = set()
                    result["transactions"][tx_type] = [
                        tx for tx in result["transactions"][tx_type]
                        if not (tx["tx_hash"] in seen_hashes or seen_hashes.add(tx["tx_hash"]))
                    ]

            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

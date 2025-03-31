import time

COMMON_HEADERS = {}

URL_META = {
    "eth": "ETHERSCAN_API_URL",
    "bsc": "BSCSCAN_API_URL",
    "tron": "TRONSCAN_API_URL",
}

KEY_META = {
    "eth": "ETHERSCAN_API_KEY",
    "bsc": "BSCSCAN_API_KEY",
    "tron": "TRONSCAN_API_KEY",
}

API_META = {
    "eth":
        {
            "normal": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey"),
                "address": [("params", "address")],
                "params": {
                    "chainid": "1",
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "txlist",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                    "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
            "token": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey",),
                "address": [("params", "address")],
                "params": {
                    "chainid": "1",
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "tokentx",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "contractAddress": lambda tx: tx['contractAddress'],
                    "tokenName": lambda tx: tx['tokenName'],
                    "tokenSymbol": lambda tx: tx['tokenSymbol'],
                    "value": lambda tx: f"{int(tx['value']) / 10 ** int(tx['tokenDecimal'])}",
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
            "nft": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey",),
                "address": [("params", "address")],
                "params": {
                    "chainid": "1",
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "tokennfttx",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "contractAddress": lambda tx: tx['contractAddress'],
                    "tokenName": lambda tx: tx['tokenName'],
                    "tokenSymbol": lambda tx: tx['tokenSymbol'],
                    "tokenID": lambda tx: tx['tokenID'],
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
            "erc1155": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey",),
                "address": [("params", "address")],
                "params": {
                    "chainid": "1",
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "token1155tx",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "contractAddress": lambda tx: tx['contractAddress'],
                    "tokenName": lambda tx: tx['tokenName'],
                    "tokenSymbol": lambda tx: tx['tokenSymbol'],
                    "tokenID": lambda tx: tx['tokenID'],
                    "tokenValue": lambda tx: tx['tokenValue'],
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            }
        },
    "bsc":
        {
            "normal": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey"),
                "address": [("params", "address")],
                "params": {
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "txlist",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                    "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
            "token": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey"),
                "address": [("params", "address")],
                "params": {
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "tokentx",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "contractAddress": lambda tx: tx['contractAddress'],
                    "tokenName": lambda tx: tx['tokenName'],
                    "tokenSymbol": lambda tx: tx['tokenSymbol'],
                    "value": lambda tx: f"{int(tx['value']) / 10 ** int(tx['tokenDecimal'])}",
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
            "nft": {
                "api_prefix": "",
                "headers": COMMON_HEADERS,
                "api_key": ("params", "apikey"),
                "address": [("params", "address")],
                "params": {
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "action": "tokennfttx",
                    "module": "account"
                },
                "format_result": True,
                "results": {
                    "tx_hash": lambda tx: f"{tx['hash']}",
                    "block": lambda tx: int(tx['blockNumber']),
                    "time": lambda tx: int(tx['timeStamp']),
                    "days_age": lambda tx: f"{(int(time.time()) - int(tx['timeStamp'])) // (24 * 3600)} days ago",
                    "from": lambda tx: tx['from'],
                    "to": lambda tx: tx['to'],
                    "contractAddress": lambda tx: tx['contractAddress'],
                    "tokenName": lambda tx: tx['tokenName'],
                    "tokenSymbol": lambda tx: tx['tokenSymbol'],
                    "tokenID": lambda tx: tx['tokenID'],
                    "type": lambda tx,
                                   address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
                },
            },
        },
    "tron": {
        "normal": {
            "api_prefix": "/transaction",
            "headers": COMMON_HEADERS,
            "api_key": ("headers", "TRON-PRO-API-KEY"),
            "address": [("params", "address")],
            "params": {
                "start": 45,
                "limit": 100,
                "start_timestamp": 0,
                # "end_timestamp": int(time.time())*1000,
                # "end_timestamp": 9999999999999
            },
            "format_result": False,
            "results": {
                "tx_hash": lambda tx: f"{tx['hash']}",
                "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                "block": lambda tx: int(tx['blockNumber']),
                "time": lambda tx: int(tx['timestamp']),
                "days_age": lambda tx: f"{(int(time.time()) - int(tx['timestamp'])) // (24 * 3600)} days ago",
                "from": lambda tx: tx['from'],
                "to": lambda tx: tx['to'],
                "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                "type": lambda tx,
                               address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
            }
        },
        "token_trc20": {
            "api_prefix": "/token_trc20/transfers",
            "headers": COMMON_HEADERS,
            "api_key": ("headers", "TRON-PRO-API-KEY"),
            "address": [("params", "address")],
            "params": {
                "limit": 10000,
                "start_timestamp": 0,
                # "end_timestamp": int(time.time())*1000,
                "end_timestamp": 9999999999999
            },
            "format_result": False,
            "results": {
                "tx_hash": lambda tx: f"{tx['hash']}",
                "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                "block": lambda tx: int(tx['blockNumber']),
                "time": lambda tx: int(tx['timestamp']),
                "days_age": lambda tx: f"{(int(time.time()) - int(tx['timestamp'])) // (24 * 3600)} days ago",
                "from": lambda tx: tx['from'],
                "to": lambda tx: tx['to'],
                "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                "type": lambda tx,
                               address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
            }
        },
        "token_trc1155": {
            "api_prefix": "/token_trc1155/transfers",
            "headers": COMMON_HEADERS,
            "api_key": ("headers", "TRON-PRO-API-KEY"),
            "address": [("params", "address")],
            "params": {
                "limit": 10000,
                "start_timestamp": 0,
                # "end_timestamp": int(time.time())*1000,
                "end_timestamp": 9999999999999
            },
            "format_result": False,
            "results": {
                "tx_hash": lambda tx: f"{tx['hash']}",
                "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                "block": lambda tx: int(tx['blockNumber']),
                "time": lambda tx: int(tx['timestamp']),
                "days_age": lambda tx: f"{(int(time.time()) - int(tx['timestamp'])) // (24 * 3600)} days ago",
                "from": lambda tx: tx['from'],
                "to": lambda tx: tx['to'],
                "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                "type": lambda tx,
                               address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
            }
        },
        "trc10": {
            "api_prefix": "/transfer",
            "headers": COMMON_HEADERS,
            "api_key": ("headers", "TRON-PRO-API-KEY"),
            "address": [("params", "address")],
            "params": {
                "limit": 10000,
            },
            "format_result": False,
            "results": {
                "tx_hash": lambda tx: f"{tx['hash']}",
                "method": lambda tx: "Contract Interaction" if tx['input'] != '0x' else "Transfer",
                "block": lambda tx: int(tx['blockNumber']),
                "time": lambda tx: int(tx['timestamp']),
                "days_age": lambda tx: f"{(int(time.time()) - int(tx['timestamp'])) // (24 * 3600)} days ago",
                "from": lambda tx: tx['from'],
                "to": lambda tx: tx['to'],
                "amount": lambda tx: f"{int(tx['value']) / 10 ** 18}" if int(tx['value']) > 0 else "0",
                "txnfee": lambda tx: f"{(lambda x: int(x['gasUsed']) * int(x['gasPrice']) / 10 ** 18)(tx):.6f}",
                "type": lambda tx,
                               address: f"{'Send' if tx['from'].lower() == address else 'Receive' if tx['to'].lower() == address else 'N/A'}",
            }
        }
    }
}

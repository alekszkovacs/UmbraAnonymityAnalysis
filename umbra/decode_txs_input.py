from helper import Access

import time
from datetime import timedelta
import json
import requests
from web3 import Web3

_access = Access()

def decode_txs_input(contract_addr: str, og_data: dict, downloaded_data: list) -> None:

    contract_txs = og_data["result"]
    
    # If an error has stopped the previous decoding
    # So every data is decoded, not just the new ones
    if "last_decoded" in og_data: # Whether it's the first time
        for d in reversed(contract_txs):
            if d["hash"] == og_data["last_decoded"]:
                n = contract_txs.index(d) + 1
                break
    # If we don't have any data yet
    else: n = 0

    contract_txs = [*contract_txs[n:], *downloaded_data]

    contract_abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_addr}&apikey={_access.ETHERSCAN_API_KEY}"
    contract_abi = json.loads(requests.get(contract_abi_endpoint).text)
    contract = _access.w3.eth.contract(address=Web3.toChecksumAddress(contract_addr), abi=contract_abi["result"])

    # contract_txs point to the undecoded txs
    n = 0
    l = len(contract_txs)
    start = time.time()

    for d in contract_txs:
        n += 1
        if d["functionName"] == "":
            now = time.time()
            print(f"{n}/{l} record(s) decoded. Elapsed time: {timedelta(seconds=now-start)}\r", end="")
            continue

        func_obj, func_params = contract.decode_function_input(d["input"])

        for key, value in func_params.items():
            if not (isinstance(value, str) or isinstance(value, int)):
                func_params[key] = str(value)  # it's bytes

        d[d["functionName"]] = func_params
        og_data["last_decoded"] = d["hash"]

        now = time.time()
        print(f"{n}/{l} record(s) decoded. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

    if l == 0:
        print("0 record decoded.")
    else:
        print()

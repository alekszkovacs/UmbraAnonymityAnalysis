import time
from datetime import timedelta
import requests
import json

from helper import Access
from helper import FunctionName as fn
from download_txs import download_txs
from get_fees import get_txs_fees


_access = Access()

def get_withdraw_txs(og_data: dict, downloaded_data: list, download_all: bool) -> None:

    contract_txs = og_data["result"]

    if download_all:
        n = 0
    else:
        # it can be the first time
        if "last_withdraw" in og_data:
            for d in reversed(contract_txs):
                if d["hash"] == og_data["last_withdraw"]:
                    # if downloaded_count == 0 -> n = 0
                    n = contract_txs.index(d) + 1
                    break
        else: n = 0

    contract_txs = [*contract_txs[n:], *downloaded_data]
    
    n = 0
    l = len(contract_txs)
    found = 0
    for d in contract_txs:
        n += 1

        if d["functionName"]== fn.S_ETH.value:
            address = d[d["functionName"]]["_receiver"]
        else:
            continue

        if download_all:
            if address in d[d["functionName"]]:
                if len(d[d["functionName"]][address]) == w3.eth.get_transaction_count(Web3.toChecksumAddress(address)):
                    og_data["last_withdraw"] = d["hash"]
                    now = time.time()
                    print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-_access.start_time)}\r", end="")
                    continue


        data = download_txs(address, 0)
        get_txs_fees(data)

        d[d["functionName"]][address] = data
        found += len(data)

        og_data["last_withdraw"] = d["hash"]
        now = time.time()
        print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-_access.start_time)}\r", end="")

    if l == 0:
        print("0 record checked for withdraw.")
    else:
        print()
        
import time
from datetime import timedelta

from helper import Access


_access = Access()


def get_txs_fees(tx: dict | list) -> None:

    if type(tx) is dict: txs = [tx]
    else: txs = tx

    for d in txs:
        temp_tx = _access.w3.eth.get_transaction(d["hash"])

        if "maxFeePerGas" in temp_tx:
            # it means it is a tx with type EIP-1559
            d["maxFeePerGas"] = temp_tx["maxFeePerGas"]
            d["maxPriorityFeePerGas"] = temp_tx["maxPriorityFeePerGas"]

def get_fees(og_data: dict, downloaded_data: list) -> None:

    contract_txs = og_data["result"]

    if "last_fee" in og_data:
        for d in reversed(contract_txs):
            if d["hash"] == og_data["last_fee"]:
                n = contract_txs.index(d) + 1
                break
    else: n = 0

    contract_txs = [*contract_txs[n:], *downloaded_data]

    print("Getting tx fees...")

    n = 0
    l = len(contract_txs)
    start = time.time()
    for d in contract_txs:
        n+=1

        get_txs_fees(d)
    
        og_data["last_fee"] = d["hash"]

        now = time.time()
        print(f"{n}/{l} records checked for priority fees. Elapsed time: {timedelta(seconds=now-start)}\r", end="")


    
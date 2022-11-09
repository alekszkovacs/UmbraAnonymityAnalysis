from helper import Access
from download_txs import download_txs

import time
from datetime import timedelta
import requests
import json

_access = Access()

def get_withdraw_txs(og_data: dict, downloaded_data: list, allb: bool) -> None:

    contract_txs = og_data["result"]

    if allb:
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
    start = time.time()

    for d in contract_txs:
        n += 1

        if d["functionName"]== "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)":
            address = d[d["functionName"]]["_receiver"]
        elif d["functionName"]== "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
            address = d[d["functionName"]]["_acceptor"]
        else:
            continue

        if allb:
            if address in d[d["functionName"]]:
                if len(d[d["functionName"]][address]) == w3.eth.get_transaction_count(Web3.toChecksumAddress(address)):
                    og_data["last_withdraw"] = d["hash"]
                    now = time.time()
                    print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")
                    continue


        data = download_txs(address, 0)
        d[d["functionName"]][address] = data
        found += len(data)

        og_data["last_withdraw"] = d["hash"]
        now = time.time()
        print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

    if l == 0:
        print("0 record checked for withdraw.")
    else:
        print()
        
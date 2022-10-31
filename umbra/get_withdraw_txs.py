from helper import Access

import time
from datetime import timedelta
from ratelimit import limits, sleep_and_retry
import requests
import json

_access = Access()

CALLS = 4
RATE_LIMIT = 1  # time period in seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    return requests.get(url)

def get_withdraw_txs(og_data: dict, downloaded_data: list, _all: bool) -> None:

    contract_txs = og_data["result"]

    if _all:
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
            _address = d[d["functionName"]]["_receiver"]
        elif d["functionName"]== "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
            _address = d[d["functionName"]]["_acceptor"]
        else:
            continue

        if _all:
            if _address in d[d["functionName"]]:
                if len(d[d["functionName"]][_address]) == w3.eth.get_transaction_count(Web3.toChecksumAddress(_address)):
                    og_data["last_withdraw"] = d["hash"]
                    now = time.time()
                    print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")
                    continue

        response = call_api(f"https://api.etherscan.io/api?module=account&action=txlist&address={_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={_access.ETHERSCAN_API_KEY}")

        if response.status_code == 200:
            data_json = response.text
            data = json.loads(data_json)
            d[d["functionName"]][_address] = data["result"]
            found += len(data["result"])

        og_data["last_withdraw"] = d["hash"]
        now = time.time()
        print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

    if l == 0:
        print("0 record checked for withdraw.")
    else:
        print()
        
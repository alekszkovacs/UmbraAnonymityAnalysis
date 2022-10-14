from ratelimit import limits, sleep_and_retry
import requests
from web3 import Web3
import json
import time
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
WEB3_WEBSOCKET_PROVIDER = os.environ["WEB3_WEBSOCKET_PROVIDER"]

w3 = Web3(Web3.WebsocketProvider(WEB3_WEBSOCKET_PROVIDER))

CALLS = 4
RATE_LIMIT = 1   # time period in seconds
    
@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    return requests.get(url)

with open("../data/function_inputs.json", "r") as file:
    sendEth = json.load(file)["sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)"]

output_dict = {}
n = 0

try:
    with open("../data/eth/withdraw_transactions_from_stealth_addresses_ETH.json", "r") as file:
        output_dict = json.load(file)
        
        start = time.time()
        for i in sendEth:
            stealth_address = i["_receiver"]
            n += 1

            if stealth_address in output_dict:
                if len(output_dict[stealth_address]["txs"]) == w3.eth.get_transaction_count(Web3.toChecksumAddress(stealth_address)):
                    now = time.time()
                    print(f"{n}/{len(sendEth)}, elapsed time {timedelta(seconds=now-start)}, no need to update")
                    continue

            response = call_api(f"https://api.etherscan.io/api?module=account&action=txlist&address={stealth_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}")

            if response.status_code == 200:
                data_json = response.text
                data = json.loads(data_json)
                output_dict[stealth_address] = {"stealth_address": stealth_address, "txs": data["result"]}

            now = time.time()
            print(f"{n}/{len(sendEth)}, elapsed time {timedelta(seconds=now-start)}, status {response.status_code}")

except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")

finally:
    with open("../data/eth/withdraw_transactions_from_stealth_addresses_ETH.json", "w") as file:
        json.dump(output_dict, file)
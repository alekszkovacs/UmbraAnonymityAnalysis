from helper import Access

import json
import requests

_access = Access()

def download_txs(contract_addr: str, lb: int) -> list:

    print(f"Getting contract transactions from block {lb}...")
    response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_addr}&startblock={lb}&endblock=99999999&page=1&offset=10000&sort=asc&apikey={_access.ETHERSCAN_API_KEY}")
    print(f"Response code: {response.status_code}")

    if int(response.status_code) == 200:
        data_json = response.text
        data = json.loads(data_json)["result"]

        if lb == 0:
            del data[0]

        print(f"Successfully downloaded {len(data)} transactions.")
    else:
        data = []
    
    return data
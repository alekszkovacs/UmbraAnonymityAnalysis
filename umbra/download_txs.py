from helper import Access

import json
import requests
from ratelimit import limits, sleep_and_retry

_access = Access()

CALLS = 4
RATE_LIMIT = 1  # time period in seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    return requests.get(url)


def download_txs(addr: str, lb: int) -> list:

    response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock={lb}&endblock=99999999&page=1&offset=10000&sort=asc&apikey={_access.ETHERSCAN_API_KEY}")

    if int(response.status_code) == 200:
        data_json = response.text
        data = json.loads(data_json)["result"]

        for d in data.copy():
            if int(d["txreceipt_status"]) == 0 or int(d["isError"] == 1):
                data.remove(d)

    else:
        data = []
    
    return data
from helper import access, Network

import json
import requests
from ratelimit import limits, sleep_and_retry


CALLS = 3
RATE_LIMIT = 1  # time period in seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    return requests.get(url)


def download_txs(addr: str, lb: int) -> list:
    downloaded_data = []
    current_data = []
    loop = True

    while loop:
   
        response = call_api(
            f"https://{access.API_ADDR}/api?module=account&action=txlist&address={addr}&startblock={lb}&endblock=9999999999999&page=1&offset=10000&sort=asc&apikey={access.API_KEY}"
        )
        if int(response.status_code) == 200:
            data_json = response.text
            current_data = json.loads(data_json)["result"]
        else: raise Exception(f"Some error occured. Unable to download txs. Error {response.status_code}")

        if downloaded_data != []:
            for d in current_data.copy():
                if d["hash"] != downloaded_data[-1]["hash"]:
                    current_data.remove(d)
                else:
                    current_data.remove(d)
                    break

        if current_data != []:
            downloaded_data = [*downloaded_data, *current_data]
            lb = current_data[-1]["blockNumber"]

            # Check wether there are more txs
            response = call_api(
                f"https://{access.API_ADDR}/api?module=account&action=txlist&address={addr}&startblock={str(int(lb)+1)}&endblock=9999999999999&page=1&offset=10000&sort=asc&apikey={access.API_KEY}"
            )
            if int(response.status_code) == 200:
                data_json = response.text
                temp_data = json.loads(data_json)["result"]
            else: raise Exception(f"Some error occured. Unable to download txs. Error {response.status_code}")

            # If there aren't more txs
            if temp_data == []: loop = False
        
        else: loop = False
    
    for d in downloaded_data.copy():
        if int(d["txreceipt_status"]) == 0 or int(d["isError"] == 1):
            downloaded_data.remove(d)

    return downloaded_data
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]

response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address=0xfb2dc580eed955b528407b4d36ffafe3da685401&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}")
print(response.status_code)

data_json = response.text
data = json.loads(data_json)

with open("../data/contract_txs.json", "w") as file:
    #json.dump(response.text, file)
    #print(response.text)
    file.write(data_json)

trx_count = len(data["result"]) - 1
print(trx_count)
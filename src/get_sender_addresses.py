import json
from collections import Counter

with open("../data/contract_txs.json", "r") as file:
    contract_txs = json.load(file)["result"] #all the transactions' details related to the umbra contract

contract_txs = contract_txs[1:]

txs_to_contract = []

for c in contract_txs:
    txs_to_contract.append(c["from"])

adresses_of_txs_to_contract_count = Counter(txs_to_contract) #count of txs grouped by address

with open("../data/sender_addresses.json", "w") as file:
    json.dump(dict(adresses_of_txs_to_contract_count), file)
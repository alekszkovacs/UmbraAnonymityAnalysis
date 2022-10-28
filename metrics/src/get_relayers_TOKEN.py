import os
import json
from collections import Counter

with open("../data/contract_txs.json", "r") as file:
    contract_txs = json.load(file)["result"] #all the transactions' details related to the umbra contract

contract_txs = contract_txs[1:]

addresses = []

for c in contract_txs:
    if c["functionName"] == "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
        addresses.append(c["from"])   

addresses_count = Counter(addresses) #count of txs grouped by address

with open("../data/relayers_TOKEN.json", "w") as file:
    json.dump(dict(addresses_count), file)
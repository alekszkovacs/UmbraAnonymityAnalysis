# When the sender address of the eth is the same as the final receiver

import json

with open("umbra/data/umbra_contract_txs.json", "r") as file:
    contract_txs = json.load(file)["result"]

chain = []
n = 0
for d in contract_txs:
    n+=1
    if d["functionName"] == "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)":
        stealth = d[d["functionName"]]["_receiver"]
        for tx in d[d["functionName"]][stealth]:
            if d["from"] == tx["to"]:
                sent_eth = int(d["value"]) / pow(10, 18)
                a_append = {"tx": d["hash"], "address": d["from"], "sent_eth": sent_eth}
                if "sender_ens" in d:
                    chain.append({**a_append, **{"ens": d["sender_ens"]}})
                else:
                    chain.append(a_append)
    elif d["functionName"] == "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
        if d["from"] == d[d["functionName"]]["_acceptor"]:
            a_append = {"tx": d["hash"], "address": d["from"], "sent_token": ""}
            if "sender_ens" in d:
                chain.append({**a_append, **{"ens": d["sender_ens"]}})
            else:
                chain.append(a_append)


with open("statistics/results/same_sender_receiver.json", "w") as file:
    json.dump(chain, file)

with open("statistics/results/same_sender_receiver_ens.json", "w") as file:
    json.dump(list(filter(lambda i: "ens" in i, chain)), file)
"""
    HEURISTICS 2:
    When the sender address of the eth/token is the same as the receiver address of the withdraw tx (from stealth address).

    This heuristics is based on the assumption that if the sender and the final receiver is the same (call it x),
    then it is highly likely that the real address behind the stealth address is x.

    #1 (jupyter)
    To be more precise regarding this heuristics we should check wether the sender and the withdrawer tx transfers the same
    amount of eth/token.
"""
import sys
import json
from collections import Counter
sys.path.append("./")

from helper import FunctionName as fn
from reports.heuristics import Heuristics

class Heuristics2(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)


    def main(self) -> None:
        print("--HEURISTICS 2--")
        same_sender_receiver = self._get_results()
        
    def _get_results(self) -> list:
        result_list = []
        n = 0
        for d in self._contract_txs:
            n+=1
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]
                for tx in d[d["functionName"]][stealth]:
                    if d["from"] == tx["to"]:
                        sent_eth = int(d["value"]) / pow(10, 18)
                        withdrawn_eth = int(tx["value"]) / pow(10, 18)
                        a_append = {
                            "tx": d["hash"],
                            "address": d["from"],
                            "sent_eth": sent_eth,
                            "withdrawn_eth": withdrawn_eth
                        }
                        if "sender_ens" in d:
                            result_list.append({**a_append, **{"ens": d["sender_ens"]}})
                        else:
                            result_list.append(a_append)
            elif d["functionName"] == fn.W_TOKEN.value:
                if d["from"] == d[d["functionName"]]["_acceptor"]:
                    a_append = {
                        "tx": d["hash"],
                        "address": d["from"],
                        "sent_token": ""
                    }
                    if "sender_ens" in d:
                        result_list.append({**a_append, **{"ens": d["sender_ens"]}})
                    else:
                        result_list.append(a_append)

        with open("reports/results/same_sender_receiver.json", "w") as file:
            json.dump(result_list, file)

        return result_list

    def _get_statistics(self, same_sender_receiver: list) -> None:







        receivers = list(map(lambda v: v["receiver_address"], receivers_in_skr))
        print(f"There are {len(receivers)}/{len(self._contract_txs)} withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.")
        # We know that every stealth address have been used only once. (umbra_statistics jupyter)
        c_receivers = Counter(receivers)
        print(f"This means we have assigned {len(receivers)} stealth addresses to {len(dict(c_receivers))} different addresses,")

        ens = list(filter(lambda v: "ens" in v, receivers_in_skr))
        ens = list(map(lambda v: v["ens"], ens))
        ens = Counter(ens)
        print(f"which from {len(dict(ens))} has ens address.")


if __name__ == "__main__":
    with open("umbra/data/umbra_contract_txs.json", "r") as file:
        data = json.load(file)
    with open("umbra/data/stealth_key_registry_contract_txs.json", "r") as file:
        skr_data = json.load(file)

    contract_txs = data["result"]
    skr_contract_txs = skr_data["result"]

    h2 = Heuristics2(contract_txs, skr_contract_txs)
    h2.main()
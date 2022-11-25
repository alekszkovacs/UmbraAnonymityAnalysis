"""
    HEURISTICS 1:
    When the receiver address of the eth/token has an address which has communicated with stealth registry.

    With this heuristics we can basically precisely determine the real address behind a stealth address.
    In some cases we can even determine the ENS address, which brings us more closer to the real person!

    As a "sideheuristics" we could simply search for ENS addresses, but it would maybe give out false
    results since the tx when someone spends his/her money paying someone with an ENS would be also included.

    #1 (jupyter)
    In this case we have to examine whether the whole amount was sent to the receiver or not.
    If yes, then we can be pretty sure about that the person behind the stealth address and the receiver address 
    is the same, since it is highly unlikely that someone has to pay exactly the same amount
    that she/he has received to someone else who has been also registrated into skr.
"""
import sys
import json
from collections import Counter
sys.path.append("./")

from helper import FunctionName as fn
from reports.heuristics import Heuristics

class Heuristics1(Heuristics):
    # This code runs in the background (if we don't write anything):
    """
    def __new__(cls, *args):
        return super().__new__(cls, *args)
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)
    """

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)


    def main(self) -> None:
        print("--HEURISTICS 1--")
        receivers_in_skr = self._get_receivers()
        self._get_statistics(receivers_in_skr)


    def _get_receivers(self) -> list:
        skr_addresses = list(map(lambda d: d["from"], self._skr_contract_txs))
        result_list = []

        for d in self._contract_txs:
            
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]
                for tx in d[d["functionName"]][stealth]:
                    if tx["to"] in skr_addresses:
                        a_append = {"sender_tx": d["hash"],
                                    "receiver_tx": tx["hash"],
                                    "receiver_address": tx["to"]}
                        if "receiver_ens" in tx:
                            result_list.append({**a_append, **{"ens": tx["receiver_ens"]}})
                        else:
                            result_list.append(a_append)

            elif d["functionName"] == fn.W_TOKEN.value:
                receiver = d[d["functionName"]]["_acceptor"]
                if receiver in skr_addresses:
                    a_append = {"sender_tx": d["hash"],
                                "receiver_tx": d["hash"],
                                "receiver_address": receiver}
                    if "receiver_ens" in d[d["functionName"]]:
                        result_list.append({**a_append, **{"ens": d[d["functionName"]]["receiver_ens"]}})
                    else:
                        result_list.append(a_append)


        with open("reports/results/receivers_in_skr.json", "w") as file:
            json.dump(result_list, file)

        return result_list

    def _get_statistics(self, receivers_in_skr: list) -> None:
        receivers = list(map(lambda v: v["receiver_address"], receivers_in_skr))
        print(f"There are {len(receivers)}/{len(self._contract_txs)} withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.")
        # We know that every stealth address have been used only once. (umbra_statistics jupyter)
        c_receivers = Counter(receivers)
        print(f"This means we have assigned {len(receivers)} stealth addresses to {len(dict(c_receivers))} different addresses,")

        ens = list(filter(lambda v: "ens" in v, receivers_in_skr))
        ens = list(map(lambda v: v["ens"], ens))
        ens = Counter(ens)
        print(f"which from {len(dict(ens))} has ens address.")
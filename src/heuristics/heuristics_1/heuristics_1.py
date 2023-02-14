import sys
from collections import Counter
import json

from src.helper import access, Network
from ..heuristics import run_single_heuristics, Heuristics
from .heuristics_1_base import Heuristics1Base


class Heuristics1(Heuristics1Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _get_statistics(self, results: list) -> set:
        """
            results is a list. An element:
            {
                "stealth":          address of stealth address
                "sender_tx":        sender tx hash
                "receiver_tx":      receiver tx hash
                "receiver_address": address of the user behind stealth
                "ens":              ens of the user
            }
        """

        with open(Heuristics.result_path+"receivers_in_skr.json", "w") as file:
            json.dump(results, file)

        receivers = list(map(lambda v: v["receiver_address"], results))
        print(f"There are `{len(receivers)}/{len(self._contract_txs)}` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.")
        c_receivers = Counter(receivers)
        print(f"This means we have assigned `{len(receivers)}` stealth addresses to `{len(dict(c_receivers))}` different addresses. ", end="")

        if access.network == Network.MAINNET:
            ens = list(filter(lambda v: "ens" in v, results))
            ens = list(map(lambda v: v["ens"], ens))
            ens = Counter(ens)
            print(f"From these `{len(dict(ens))}` has ens address.")

        return results

    def _return_stealths(self, statistics) -> dict:
        """
            statistics is a list. An element:
            {
                "stealth":          address of stealth address
                "sender_tx":        sender tx hash
                "receiver_tx":      receiver tx hash
                "receiver_address": address of the user behind stealth
                "ens":              ens of the user
            }
        """

        stealths = {}
        for d in statistics:
            temp = {
                "underlying": d["receiver_address"]
            }
            if access.network == Network.MAINNET and "ens" in d:
                stealths[d["stealth"]] = {**temp, **{"ens": d["ens"]}}
            else:
                stealths[d["stealth"]] = temp


        return {"deanonymized": stealths}


if __name__ == "__main__":
    run_single_heuristics(Heuristics1)
    
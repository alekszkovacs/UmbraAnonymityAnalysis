import sys
from collections import Counter
sys.path.append("./")

from helper import access, Network
from reports.heuristics.heuristics import run_single_heuristics
from reports.heuristics.heuristics_2.heuristics_2_base import Heuristics2Base


class Heuristics2(Heuristics2Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _get_statistics(self, results: list) -> set:
        """
            results is a list. An element:
            {
                "stealth":  address of stealth address
                "tx":       tx hash
                "address":  address of the user behind stealth
                "ens":      ens of the user
            }
        """
        
        same = list(map(lambda v: v["address"], results))
        print(f"There are `{len(same)}/{len(self._contract_txs)}` addresses who have sent funds to themselves.")
        # We know that every stealth address have been used only once. (umbra_statistics jupyter)
        c_same = Counter(same)
        print(f"This means we have assigned `{len(same)}` stealth addresses to `{len(dict(c_same))}` different addresses,")

        if access.network == Network.MAINNET:
            ens = list(filter(lambda v: "sender_ens" in v, results))
            ens = list(map(lambda v: v["sender_ens"], ens))
            ens = Counter(ens)
            print(f"which from `{len(dict(ens))}` has ens address.")

        return results

    def _return_stealths(self, statistics) -> dict:
        """
            statistics is a list. An element:
            {
                "stealth":  address of stealth address
                "tx":       tx hash
                "address":  address of the user behind stealth
                "ens":      ens of the user
            }
        """

        stealths = {}
        for d in statistics:
            temp = {
                "underlying": d["address"]
            }
            if access.network == Network.MAINNET and "ens" in d:
                stealths[d["stealth"]] = {**temp, **{"ens": d["ens"]}}
            else:
                stealths[d["stealth"]] = temp


        return {"deanonymized": stealths}


if __name__ == "__main__":
    run_single_heuristics(Heuristics2)
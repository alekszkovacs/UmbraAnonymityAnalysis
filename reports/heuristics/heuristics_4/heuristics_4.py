import sys
from collections import Counter
sys.path.append("./")

from helper import access, Network
from reports.heuristics.heuristics import run_single_heuristics
from reports.heuristics.heuristics_4.heuristics_4_base import Heuristics4Base


class Heuristics4(Heuristics4Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _get_statistics(self, results: dict) -> set:
        fees = []
        for fee, addresses in results.items():
            sender = False
            withdrawal = False
            for ad in addresses:
                if sender and withdrawal:
                    fees.append(fee)
                    break
                if ad["type"] == "send":
                    sender = True
                if ad["type"] == "withdraw":
                    withdrawal = True

        print(f"Fees where there's both sender and withdrawal tx: {fees}")

        match access.network:
            
            case Network.MAINNET:
                print("\nSadly all of the fees are some rounded values and we definitely can't say that they are unique, ", end="")
            
            case Network.POLYGON:
                print("\nNo fee was found where there's both sender and withdrawal tx, ", end="") 

        print("so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.")

        return set()

    def _return_stealths(self, statistics) -> dict:
        return {"deanonymized": statistics}


if __name__ == "__main__":
    run_single_heuristics(Heuristics4)
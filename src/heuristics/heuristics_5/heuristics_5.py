import sys
from collections import Counter
import json

from src.helper import access, Network
from ..heuristics import run_single_heuristics, Heuristics
from .heuristics_5_base import Heuristics5Base


class Heuristics5(Heuristics5Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _get_statistics(self, results: dict) -> set:

        with open(Heuristics.result_path+"addresses_by_fees.json", "w") as file:
            json.dump(results, file)

        fees = []
        for fee, addresses in results.items():
            sender = False
            withdrawal = False
            for ad in addresses:
                if ad["type"] == "send":
                    sender = True
                if ad["type"] == "withdraw":
                    withdrawal = True
                if sender and withdrawal:
                    fees.append(fee)
                    break

        print(f"Fees where there's both sender and withdrawal tx: {fees}")

        match access.network:
            
            case Network.MAINNET:
                print("\nSadly all of the fees are some rounded values and we definitely can't say that they are unique, ", end="")
            
            case Network.POLYGON:
                print("\nNo fee was found where there's both sender and withdrawal tx, ", end="") 

            case _:
                print(fees)

        print("so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.")

        return set()

    def _return_stealths(self, statistics) -> dict:
        return {"deanonymized": statistics}


if __name__ == "__main__":
    run_single_heuristics(Heuristics4)
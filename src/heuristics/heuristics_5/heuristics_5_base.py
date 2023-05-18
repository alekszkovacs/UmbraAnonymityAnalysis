"""
    HEURISTICS 5:
    If the recipient address r on a network is already registered in the Umbra Stealth Key Registry in a different
    network, then we link the recipient address to the registrant address on the other network.
"""

import sys
import json

from src.helper import FunctionName as fn
from ..heuristics import Heuristics


class Heuristics5Base(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _print_intro(self) -> None:
        print("\n## HEURISTICS 5\n")
        
    def _get_results(self) -> dict:
        result_dict = {}

        for d in self._contract_txs:
            if "maxPriorityFeePerGas" in d:
                # it means it is a tx with type EIP-1559

                ### heuristics_4 --> ###
                #1
                if d["functionName"] == fn.W_TOKEN.value:
                    continue
                ### heuristics_4 ###

                if d["maxPriorityFeePerGas"] not in result_dict:
                    result_dict[d["maxPriorityFeePerGas"]] = []

                temp_append = {
                    "address": d["from"],    # address which can be behind a stealth address
                    "type": "send"
                }

                result_dict[d["maxPriorityFeePerGas"]].append(temp_append)

                if d["functionName"] == fn.S_ETH.value:
                    receiver = d[d["functionName"]]["_receiver"]

                    for tx in d[d["functionName"]][receiver]:
                        if "maxPriorityFeePerGas" in tx:
                            if tx["maxPriorityFeePerGas"] not in result_dict:
                                result_dict[tx["maxPriorityFeePerGas"]] = []

                            temp_append = {
                                "address": tx["from"],  # stealth
                                "type": "withdraw",
                            }

                            result_dict[tx["maxPriorityFeePerGas"]].append(temp_append)

        for d in self._skr_contract_txs:
            if "maxPriorityFeePerGas" in d:
                # it means it is a tx with type EIP-1559

                if d["maxPriorityFeePerGas"] not in result_dict:
                    result_dict[d["maxPriorityFeePerGas"]] = []

                temp_append = {
                    "address": d["from"],
                    "type": "send"
                }

                result_dict[d["maxPriorityFeePerGas"]].append(temp_append)


        return result_dict

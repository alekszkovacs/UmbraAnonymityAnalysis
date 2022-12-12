"""
    HEURISTICS 4:
    When stealth addresses have sent their funds to different receiver addresses with the same UNIQUE, PARTICULAR
    maxPriorityFeePerGas.

    This heuristics says that if the maxPriorityFeePerGas of two or more withdraw txs is a special unique number (cannot
    be divided with 10, 100, 1000, ..., so with 10^n (n >= 1 integer)), then the person behind the stealth addresses
    which executed these txs has to be the same.

    This can happen when someone wants to collect their received funds from it's stealth addresses to other addresses
    where he/she maybe has more money or from those addresses wants to collect the funds to a joint address, but since
    he/she wants to be careful, this collection will happen after several tx level, etc.
    Since this Umbra user wanted to use Umbra correctly, he/she had withdrawn his/her funds from his/her
    stealth addresses to different addresses every time (so a receiver address is only used once), but forgot to modify
    his/her never changing priority fee in it's wallet. Or maybe had used the same receiver address more, but after that
    switched to a new receiver address for more security, but left the priority fee unchanged...

    The point is that this max priority fee value is not changing. Only the max fee per gas is changing based on the 
    current base fee of the ethereum. Because of that if once someone have chosen a special value and not changed it,
    there is a very high chance that behind another tx with the same unique value stands the same person.

    ### heuristics_4 --> ###
    #1
        Tokens are withdrawn via a smart contract function which ueses sponsorFees. Because the only used function for it
        is the "withdrawTokenOnBehalf()", all the token txs are made from a so called relayer address, and for all the 
        token txs users have to give a sponsor and a sponsorFee. There's even no maxPriorityFeePerGas for these txs.

        Because of it we should search for any kind of connection between sponsorFee and maxPriorityFeePerGas.

        The results are documented in the referenced notebook, we act according to that.
    Based on the results, we won't deal with token txs in this heuristics.

    ### common_statistics --> ###
    #2 
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the stealth addresses is the same like between
        the receivers (with the same priority fee).
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx. But
        since in this heuristics we don't deal with tokens, we don't need to check it for tokens.

        The results are documented in the referenced notebook, we act according to that.
    Based on the results we eliminated the unwanted txs.

    For this heuristics we have to collect the priority fees from the umbra txs both from the sender and the withdrawal
    side, and also from the stealth key registry txs. After that a stealth address with a given withdrawal priority fee 
    will belong to a sender (umbra) or a registrant (skr) address with the same sender or registrant priority fee.
    When we collect the sender side txs we can also collect the token ones since they also carry some information within
    themselves.

    WITH THIS HEURISTICS WE CAN ASSIGN A REAL ADDRESS TO A STEALTH ADDRESS WITH HIGH CERTAINTY.

    FUTURE IMPROVEMENTS:
        TODO:   Get the txs of the receiver addresses with same priority fee and check if we can identify a collector
                pattern using those txs. It's a deeper analysis but a  good assumption since if someone tries to collect
                it's funds, then after using the umbra correctly (one receiver address is only for one stealth) maybe
                he/she wants to collect the funds to a joint address.
"""

import sys
import json
from collections import Counter
from datetime import datetime
import pandas as pd
sys.path.append("./")

from helper import FunctionName as fn
from reports.polygon.heuristics import Heuristics


class Heuristics4(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)


    def main(self, deanonymized_stealths: dict = {}) -> dict:
        self._deanonymized_stealths = deanonymized_stealths
        print("\n## HEURISTICS 4\n")
        addresses_by_fees = self._get_results()
        self._get_statistics(addresses_by_fees)

        return {"high": set()}
        
    def _get_results(self) -> list:
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


        with open("reports/polygon/results/addresses_by_fees.json", "w") as file:
            json.dump(result_dict, file)

        return result_dict

    def _get_statistics(self, addresses_by_fees: dict) -> None:
        fees = []
        for fee, addresses in addresses_by_fees.items():
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

        print(f"Fees where there's both sender and withdrawal txs: {fees}")

if __name__ == "__main__":
    with open("umbra/data/polygon/umbra_contract_txs.json", "r") as file:
        data = json.load(file)
    with open("umbra/data/polygon/stealth_key_registry_contract_txs.json", "r") as file:
        skr_data = json.load(file)

    contract_txs = data["result"]
    skr_contract_txs = skr_data["result"]

    h4 = Heuristics4(contract_txs, skr_contract_txs)
    h4.main()
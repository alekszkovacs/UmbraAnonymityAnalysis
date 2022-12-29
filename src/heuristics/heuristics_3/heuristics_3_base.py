"""
    HEURISTICS 3:
    When different stealth addresses have sent their funds directly to the same address. Eth and token txs are handled
    together.

    This heuristics is based on the assumption that if there are txs from several stealth addresses to the same receiver
    address, then it could be that the receiver is the owner of the stealth addresses. 

    There is only one problem with this: what if the receiver is someone who gives some kind of service in exchange of
    money and people with stealth address are paying for him/her? It could make sense in two cases:
        - When someone sends his/her own money to stealth addresses owned by him-/herself, and from those stealth
          addresses sends money to the service.
        - When someone gets funds to a stealth address, and wants to pay to someone with it.
    Anyhow, since it is a heuristics, we don't say that the results are 100% sure, it can contain false positives. For
    eliminating these, we should make a more deeper analysis, but we won't do it yet.

    ### common_statistics --> ###
    #2 
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was a tx where someone payed to someone else.
        With this we can make the anonymity set smaller.
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx.

        The results are documented in the referenced notebook, we act according to that.
    Based on the results we eliminated the unwanted txs.

    This point #2 in common_statistics gives us high chance to the correctness of this heuristics since if we only deal
    with stealth addresses where the whole amount was withdrawn in one tx, it is likely that the owners of the stealth
    addresses outsource their funds the a common address where they can pile it up.

    WITH THIS HEURISTICS WE CAN CONNECT STEALTH ADDRESSES TOGETHER.
"""
import sys
import json
from collections import Counter
from datetime import datetime

from src.helper import FunctionName as fn
from src.helper import access, Network
from ..heuristics import Heuristics


class Heuristics3Base(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _print_intro(self) -> None:
        print("\n## HEURISTICS 3\n")
        
    def _get_results(self) -> dict:
        result_dict = {}

        for d in self._contract_txs:
            
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]
                sent_eth = int(d["value"])
                
                for tx in d[d["functionName"]][stealth]:
                    
                    if tx["to"] not in result_dict: 
                        result_dict[tx["to"]] = {}
                        if access.network == Network.MAINNET and "receiver_ens" in tx: result_dict[tx["to"]]["ens"] = tx["receiver_ens"]
                        result_dict[tx["to"]]["collection_count"] = 0
                        result_dict[tx["to"]]["stealths"] = []

                    result_dict[tx["to"]]["stealths"].append({
                        "stealth": stealth,
                        "withdrawn_time": datetime.fromtimestamp(int(tx["timeStamp"])).strftime("%Y.%m.%d, %H:%M:%S"),
                        "amount": sent_eth/pow(10, 18)
                    })
                    result_dict[tx["to"]]["collection_count"] += 1

            elif d["functionName"] == fn.W_TOKEN.value:
                func = d[d["functionName"]]
                receiver = func["_acceptor"]

                if receiver not in result_dict: 
                    result_dict[receiver] = {}
                    if access.network == Network.MAINNET and "receiver_ens" in func: result_dict[receiver]["ens"] = func["receiver_ens"]
                    result_dict[receiver]["collection_count"] = 0
                    result_dict[receiver]["stealths"] = []

                result_dict[receiver]["stealths"].append({
                        "stealth": func["_stealthAddr"],
                        "withdrawn_time": datetime.fromtimestamp(int(d["timeStamp"])).strftime("%Y.%m.%d, %H:%M:%S"),
                    })
                result_dict[receiver]["collection_count"] += 1


        with open(Heuristics.result_path+"collector_pattern.json", "w") as file:
            json.dump(result_dict, file)

        return result_dict
"""
    HEURISTICS 2:
    When the sender address of the eth/token is the same as the receiver address of the withdraw tx (from stealth address).

    This heuristics is based on the assumption that if the sender and the final receiver is the same (call it x), then it
    is highly likely that the real address behind the stealth address is x.

    ### common_statistics --> ###
    #2 
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the sender, stealth and receiver address is the
        same.
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx.

        The results are documented in the referenced notebook, we act according to that.
    Based on the results we eliminated the unwanted txs.

    WITH THIS HEURISTICS WE CAN ASSIGN A REAL ADDRESS TO A STEALTH ADDRESS WITH HIGH CERTAINTY.
"""
import sys
import json
sys.path.append("./")

from helper import FunctionName as fn
from helper import access, Network
from reports.heuristics.heuristics import Heuristics


class Heuristics2Base(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _print_intro(self) -> None:
        print("\n## HEURISTICS 2\n")
        
    def _get_results(self) -> list:
        result_list = []
        n = 0
        for d in self._contract_txs:
            n+=1
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]

                for tx in d[d["functionName"]][stealth]:

                    if d["from"] == tx["to"]:
                        a_append = {
                            "stealth": stealth,
                            "tx": d["hash"],
                            "address": d["from"],
                        }
                        if access.network == Network.MAINNET and "sender_ens" in d:
                            result_list.append({**a_append, **{"ens": d["sender_ens"]}})
                        else:
                            result_list.append(a_append)

            elif d["functionName"] == fn.W_TOKEN.value:
                if d["from"] == d[d["functionName"]]["_acceptor"]:
                    a_append = {
                        "stealth": d[d["functionName"]]["_stealthAddr"],
                        "tx": d["hash"],
                        "address": d["from"],
                    }
                    if access.network == Network.MAINNET and "sender_ens" in d:
                        result_list.append({**a_append, **{"ens": d["sender_ens"]}})
                    else:
                        result_list.append(a_append)

        with open(Heuristics.result_path+"same_sender_receiver.json", "w") as file:
            json.dump(result_list, file)

        return result_list

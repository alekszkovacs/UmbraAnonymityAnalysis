"""
    HEURISTICS 1:
    When the receiver address of the eth/token has an address which has communicated with stealth registry.

    This heuristics says that we can determine the receiver address behind a stealth address.
    In some cases we can even determine the ENS address (on mainnet), which brings us more closer to the real person 
    holding the receiver address!

    ### common_statistics --> ###
    #2
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the stealth and the receiver address is the same,
        since it is highly unlikely that someone has to pay exactly the same amount that she/he has received to someone
        else who has been also registrated into skr.

        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address, especially if more of
        them have communicated with the stealth key registry.

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


class Heuristics1Base(Heuristics):
    # This code runs in the background (if we don't write anything):
    """
    def __new__(cls, *args):
        return super().__new__(cls, *args)
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)
    """

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _print_intro(self) -> None:
        print("\n## HEURISTICS 1\n")

    def _get_results(self) -> list:
        skr_addresses = list(map(lambda d: d["from"], self._skr_contract_txs))
        result_list = []

        for d in self._contract_txs:
            
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]

                for tx in d[d["functionName"]][stealth]:

                    if tx["to"] in skr_addresses:
                        a_append = {
                            "stealth": stealth,
                            "sender_tx": d["hash"],
                            "receiver_tx": tx["hash"],
                            "receiver_address": tx["to"]  
                        }
                        if access.network == Network.MAINNET and "receiver_ens" in tx:
                            result_list.append({**a_append, **{"ens": tx["receiver_ens"]}})
                        else:
                            result_list.append(a_append)

            elif d["functionName"] == fn.W_TOKEN.value:
                receiver = d[d["functionName"]]["_acceptor"]
                if receiver in skr_addresses:
                    a_append = {
                        "stealth": d[d["functionName"]]["_stealthAddr"],
                        "sender_tx": d["hash"],
                        "receiver_tx": d["hash"],
                        "receiver_address": receiver
                    }
                    if access.network == Network.MAINNET and "receiver_ens" in d[d["functionName"]]:
                        result_list.append({**a_append, **{"ens": d[d["functionName"]]["receiver_ens"]}})
                    else:
                        result_list.append(a_append)

        print(Heuristics.result_path)
        with open(Heuristics.result_path+"receivers_in_skr.json", "w") as file:
            json.dump(result_list, file)

        return result_list

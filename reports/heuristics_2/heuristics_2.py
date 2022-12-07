"""
    HEURISTICS 2:
    When the sender address of the eth/token is the same as the receiver address of the withdraw tx (from stealth address).

    This heuristics is based on the assumption that if the sender and the final receiver is the same (call it x), then it
    is highly likely that the real address behind the stealth address is x.

    ### common_statistics --> ###
    #2 
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was really a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the sender, stealth and receiver address is the
        same.
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx.

        The results are documented in #2, we act according to that.

    WITH THIS HEURISTICS WE CAN ASSIGN A REAL ADDRESS TO A STEALTH ADDRESS.
"""
import sys
import json
from collections import Counter
sys.path.append("./")

from helper import FunctionName as fn
from reports.heuristics import Heuristics


class Heuristics2(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)


    def main(self, deanonymized_stealths: dict = {}) -> dict:
        print("\n## HEURISTICS 2\n")
        same_sender_receiver = self._get_results()
        self._get_statistics(same_sender_receiver)

        stealths = set(map(lambda v: v["stealth"], same_sender_receiver))
        return {"confident": stealths}

        
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
                        if "sender_ens" in d:
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
                    if "sender_ens" in d:
                        result_list.append({**a_append, **{"ens": d["sender_ens"]}})
                    else:
                        result_list.append(a_append)

        with open("reports/results/same_sender_receiver.json", "w") as file:
            json.dump(result_list, file)

        return result_list

    def _get_statistics(self, same_sender_receiver: list) -> None:
        same = list(map(lambda v: v["address"], same_sender_receiver))
        print(f"There are `{len(same)}/{len(self._contract_txs)}` addresses who have sent funds to themselves.")
        # We know that every stealth address have been used only once. (umbra_statistics jupyter)
        c_same = Counter(same)
        print(f"This means we have assigned `{len(same)}` stealth addresses to `{len(dict(c_same))}` different addresses,")

        ens = list(filter(lambda v: "sender_ens" in v, same_sender_receiver))
        ens = list(map(lambda v: v["sender_ens"], ens))
        ens = Counter(ens)
        print(f"which from `{len(dict(ens))}` has ens address.")


if __name__ == "__main__":
    with open("umbra/data/umbra_contract_txs.json", "r") as file:
        data = json.load(file)

    contract_txs = data["result"]

    h2 = Heuristics2(contract_txs, [])
    h2.main()
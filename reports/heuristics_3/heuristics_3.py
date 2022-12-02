"""
    HEURISTICS 3:
    When different stealth addresses have sent their funds directly to the same address. Eth and token txs are handled
    together.

    This heuristics is based on the assumption that if there are txs from several stealth addresses to the same receiver
    address, then it could be that the receiver is the owner of the stealth addresses. 

    There is only one problem with this: what if the receiver is someone who gives some kind of service in exchange of
    money and people with stealth address are paying for him/her? It could make sense in two cases:
        - When someone sends his/her own money to stealth addresses owned by him-/herself, and from those stealth
          addresses sends money to the service. In this case the senders should be the same.
          However, it can also happen that there is the same person behind different sender addresses associated with
          the same receiver address, but we can't find these addresses.
          Because of these, we will try to examine and search for the same sender addresses.
        - When someone gets funds to a stealth address, and wants to pay to someone with it.

    ### common_statistics --> ###
    #2 
        In this case we have to examine whether the whole amount was sent from the stealth to the receiver or not, since
        if not, then there's a higher chance that it was really a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the stealth and receiver address is the same.
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx.

        The results are documented in #2, we act according to that.

    WITH THIS HEURISTICS WE CAN CONNECT STEALTH ADDRESSES TOGETHER, BUT IT WOULD BE HARD TO SAY THAT BASED ON IT WE CAN
    DEANONYMIZE SOMEONE. Thare are too many possibilities with which we can explain a case. However there are some patterns
    which can make us some really good connections and deanonymization closely results.
"""
import sys
import json
from collections import Counter
from datetime import datetime
import pandas as pd
sys.path.append("./")

from helper import FunctionName as fn
from reports.heuristics import Heuristics

class Heuristics3(Heuristics):
    
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)


    def main(self) -> set:
        print("\n--HEURISTICS 3--")
        collector_pattern = self._get_results()
        self._get_statistics(collector_pattern)

        # stealths = set(map(lambda v: v["stealth"], same_sender_receiver))
        # return stealths

        
    def _get_results(self) -> list:
        collector_pattern = {}

        for d in self._contract_txs:
            
            if d["functionName"] == fn.S_ETH.value:
                stealth = d[d["functionName"]]["_receiver"]

                # We only have the txs where the sent and withdrawn eth are the same, so it can be used as "withdrawn eth"
                sent_eth = int(d["value"])
                
                for tx in d[d["functionName"]][stealth]:
                    
                    if tx["to"] not in collector_pattern: 
                        collector_pattern[tx["to"]] = {}
                        if "receiver_ens" in tx: collector_pattern[tx["to"]]["ens"] = tx["receiver_ens"]
                        collector_pattern[tx["to"]]["collection_count"] = 0
                        collector_pattern[tx["to"]]["stealths"] = []

                    collector_pattern[tx["to"]]["stealths"].append({
                        "sender": d["from"],
                        "stealth": stealth,
                        "withdrawn_time": datetime.fromtimestamp(int(tx["timeStamp"])).strftime("%Y.%m.%d, %H:%M:%S"),
                        "amount": sent_eth/pow(10, 18)
                    })
                    collector_pattern[tx["to"]]["collection_count"] += 1

            elif d["functionName"] == fn.W_TOKEN.value:
                func = d[d["functionName"]]
                receiver = func["_acceptor"]

                if receiver not in collector_pattern: 
                    collector_pattern[receiver] = {}
                    if "receiver_ens" in func: collector_pattern[receiver]["ens"] = func["receiver_ens"]
                    collector_pattern[receiver]["collection_count"] = 0
                    collector_pattern[receiver]["stealths"] = []

                collector_pattern[receiver]["stealths"].append({
                        "sender": d["from"],
                        "stealth": func["_stealthAddr"],
                        "withdrawn_time": datetime.fromtimestamp(int(d["timeStamp"])).strftime("%Y.%m.%d, %H:%M:%S"),
                    })
                collector_pattern[receiver]["collection_count"] += 1


        # with open("reports/results/collector_pattern.json", "w") as file:
        #     json.dump(collector_pattern, file)

        return collector_pattern

    def _get_statistics(self, collector_pattern: list) -> None:

        statistics = {}

        for receiver, values in collector_pattern.items():
            if values["collection_count"] not in statistics:
                statistics[values["collection_count"]] = []

            senders = {}
            for s in values["stealths"]:
                if s["sender"] not in senders:
                    senders[s["sender"]] = 0

                senders[s["sender"]] += 1

            result = Counter(senders.values())

            appendict = {"receiver": receiver, **dict(result)}
            if "ens" in values:
                appendict = {"ens": values["ens"], **appendict}

            statistics[values["collection_count"]].append(appendict)

        # We can't do anything with this data
        statistics.pop("1")

        with open("reports/results/collector_pattern_statistics.json", "w") as file:
            json.dump(statistics, file)

        # amounts = list(map(lambda d: d["collection_count"], collector_pattern.values()))
        # amounts = pd.Series(amounts)
        # amounts_count = amounts.value_counts()
        # df = pd.DataFrame({"Number of addresses...": amounts_count.values, "...with this many txs": amounts_count.index})

        # print(df)


if __name__ == "__main__":
    with open("umbra/data/umbra_contract_txs.json", "r") as file:
        data = json.load(file)
    with open("umbra/data/stealth_key_registry_contract_txs.json", "r") as file:
        skr_data = json.load(file)

    contract_txs = data["result"]
    skr_contract_txs = skr_data["result"]

    h3 = Heuristics3(contract_txs, skr_contract_txs)
    h3.main()
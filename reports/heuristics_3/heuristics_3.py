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
        if not, then there's a higher chance that it was really a tx where someone payed to someone else.
        If yes, then we can be pretty sure about that the person behind the stealth addresses is the same like the common
        receiver.
        
        Checking this is also good for eliminating the cases when there are more outgoing txs from a stealth address.
        In these cases we can't tell who is the real receiver and who holds the stealth address.

        We only need to check it in case of eth txs, because at tokens you must withdraw all the amount in one tx.

        The results are documented in #2, we act according to that.

    This point #2 in common_statistics gives us high chance to the correctness of this heuristics since if we only deal
    with stealth addresses where the whole amount was withdrawn in one tx, it is likely that the owners of the stealth
    addresses outsource their funds the a common address where they can pile it up.

    WITH THIS HEURISTICS WE CAN ASSIGN A REAL ADDRESS TO A STEALTH ADDRESS.
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


    def main(self, deanonymized_stealths: dict = {}) -> dict:
        self._deanonymized_stealths = deanonymized_stealths
        print("\n## HEURISTICS 3\n")
        collector_pattern = self._get_results()
        stealths = self._get_statistics(collector_pattern)

        return {"maybe": stealths}

        
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
                        "stealth": func["_stealthAddr"],
                        "withdrawn_time": datetime.fromtimestamp(int(d["timeStamp"])).strftime("%Y.%m.%d, %H:%M:%S"),
                    })
                collector_pattern[receiver]["collection_count"] += 1


        with open("reports/results/collector_pattern.json", "w") as file:
            json.dump(collector_pattern, file)

        return collector_pattern

    def _get_statistics(self, collector_pattern: list) -> set:

        # statistics = {}

        # for receiver, values in collector_pattern.items():
        #     if values["collection_count"] not in statistics:
        #         statistics[values["collection_count"]] = []

        #     senders = {}
        #     for s in values["stealths"]:
        #         if s["sender"] not in senders:
        #             senders[s["sender"]] = 0

        #         senders[s["sender"]] += 1

        #     result = Counter(senders.values())

        #     appendict = {"receiver": receiver, **dict(result)}
        #     if "ens" in values:
        #         appendict = {"ens": values["ens"], **appendict}

        #     statistics[values["collection_count"]].append(appendict)

        # # We can't do anything with this data
        # statistics.remove("1")

        # with open("reports/results/collector_pattern_statistics.json", "w") as file:
        #     json.dump(statistics, file)

        amounts = list(map(lambda d: d["collection_count"], collector_pattern.values()))
        amounts = pd.Series(amounts)
        amounts_count = amounts.value_counts()
        df = pd.DataFrame({"# of addresses": amounts_count.values, "with this many txs": amounts_count.index})

        print(df.to_markdown())

        good_users = []
        bad_users = []
        for receiver, values in collector_pattern.items():
            if values["collection_count"] == 1:
                good_users.append(values["stealths"][0]["stealth"])
            else:
                bad_users.append(object)

        print("\nThose, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. ", end="")
        print(f"There are `{len(good_users)}` addresses like this.")

        num_of_bad_good_users = 0
        for s in self._deanonymized_stealths["confident"]:
            if s in good_users:
                num_of_bad_good_users += 1

        print(f"From this we have already deanonymized `{num_of_bad_good_users}` stealth addresses, so there are only `{len(good_users) - num_of_bad_good_users}` good users.")
        print("So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. ", end="")
        print("Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:\n")

        limit = 10
        count = limit_count = 0
        print(f"We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> {limit}*.")
        for receiver, values in collector_pattern.items():
            if values["collection_count"] > limit:
                for s in values["stealths"]:
                    limit_count += 1
                    if s["stealth"] in self._deanonymized_stealths["confident"]:
                        count += 1

        print(f"There are `{count}` stealths like this out of `{limit_count}` stealths.")
        print(f"This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. ", end="")
        print("We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized ", end="")
        print("or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).")
        print("Neither one is really good or precise, so we will introduce a new unit and say that these addresses are deanonymized but with a lower certainty.")

        stealths = []
        for receiver, values in collector_pattern.items():
            if values["collection_count"] > 1:
                for s in values["stealths"]:
                    stealths.append(s["stealth"])

        print(f"There are `{len(stealths)}` addresses who has a *collection_count* *> 1*, which from ", end="")

        for s in stealths.copy():
            if s in self._deanonymized_stealths["confident"]:
                stealths.remove(s)

        print(f"`{len(stealths)}` haven't been already deanonymized. So these are the newly deanonymized with lower certainty.")

        return stealths

if __name__ == "__main__":
    with open("umbra/data/umbra_contract_txs.json", "r") as file:
        data = json.load(file)
    with open("umbra/data/stealth_key_registry_contract_txs.json", "r") as file:
        skr_data = json.load(file)

    contract_txs = data["result"]
    skr_contract_txs = skr_data["result"]

    h3 = Heuristics3(contract_txs, [])
    h3.main()
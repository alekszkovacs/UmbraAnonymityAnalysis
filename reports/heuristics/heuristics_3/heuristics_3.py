import sys
import pandas as pd
sys.path.append("./")

from reports.heuristics.heuristics import run_single_heuristics
from reports.heuristics.heuristics_3.heuristics_3_base import Heuristics3Base

class Heuristics3(Heuristics3Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)

    def _get_statistics(self, results: dict) -> set:
        """
            results is a dict. An element:

            address of the collector (the common receiver): {
                "ens": ens of the receiver
                "collection_count": how many stealths sent tx to him/her
                "stealths": [
                    {
                        "stealth":          address of stealth address
                        "withdrawn_time":   time of withdrawal
                        "amount":           withdrawn eth
                    },
                    {
                        "stealth":          address of stealth address
                        "withdrawn_time":   time of withdrawal
                        "amount":           withdrawn eth
                    }
                ]
            }
        """


        amounts = list(map(lambda d: d["collection_count"], results.values()))
        amounts = pd.Series(amounts)
        amounts_count = amounts.value_counts()
        df = pd.DataFrame({"# of addresses": amounts_count.values, "with this many txs": amounts_count.index})

        print(df.to_markdown())

        good_users = []
        bad_users = []
        for receiver, values in results.items():
            if values["collection_count"] == 1:
                good_users.append(values["stealths"][0]["stealth"])
            else:
                bad_users.append(object)

        print("\nThose, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. ", end="")
        print(f"There are `{len(good_users)}` addresses like this.")

        num_of_bad_good_users = 0
        for s in self._deanonymized_stealths["deanonymized"].keys():
            if s in good_users:
                num_of_bad_good_users += 1

        print(f"From this we have already deanonymized `{num_of_bad_good_users}` stealth addresses, so there are only `{len(good_users) - num_of_bad_good_users}` good users.")
        print("So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. ", end="")
        print("Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:\n")

        limit = 10
        count = limit_count = 0
        print(f"We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> {limit}*.")
        for receiver, values in results.items():
            if values["collection_count"] > limit:
                for s in values["stealths"]:
                    limit_count += 1
                    if s["stealth"] in self._deanonymized_stealths["deanonymized"].keys():
                        count += 1

        print(f"There are `{count}` stealths like this out of `{limit_count}` stealths.")
        print(f"This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. ", end="")
        print("We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized ", end="")
        print("or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).")
        print("Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. ", end="")
        print("Because of that we will connect these addresses together and state that these stealth addresses have common receivers, ", end="")
        print("and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of ", end="")
        print("relation among them.")

        bad_users = {}
        stealths = []
        for receiver, values in results.items():
            if values["collection_count"] > 1:
                bad_users[receiver] = values
                for s in values["stealths"]:
                    stealths.append(s["stealth"])

        print(f"There are `{len(stealths)}` receiver addresses who has a *collection_count* *> 1*, which from ", end="")

        num_of_deanonymized = 0
        for receiver, values in bad_users.items():
            for s in values["stealths"]:
                if s["stealth"] in self._deanonymized_stealths["deanonymized"].keys():
                   num_of_deanonymized+=1


        print(f"`{num_of_deanonymized}` stealth addresses have been already deanonymized. However we will include these deanonymized ones to ", end="")
        print("the connections since it carries more information.")

        return results
            
    def _return_stealths(self, statistics) -> dict:

        return_this_dict = {}
    
        for receiver, values in statistics.items():
            stealths = list(map(lambda s: s["stealth"], values["stealths"]))

            return_this_dict[receiver] = {}

            for s in stealths:
                return_this_dict[receiver][s] = None
    

        return {"connected": return_this_dict} 

if __name__ == "__main__":
    run_single_heuristics(Heuristics3)
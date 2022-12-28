import sys
import json
import copy
import importlib
sys.path.append("./")
sys.dont_write_bytecode = True # Prevent the creation of __pycache__ directories

from helper import FunctionName as fn
from helper import Network, access
from reports.heuristics.heuristics import Heuristics
from reports.heuristics.heuristics_1.heuristics_1 import Heuristics1
from reports.heuristics.heuristics_2.heuristics_2 import Heuristics2
from reports.heuristics.heuristics_3.heuristics_3 import Heuristics3
from reports.heuristics.heuristics_4.heuristics_4 import Heuristics4


class MyStatistics(object):
    _instance = None


    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self):
        super().__init__()

        self._deanonymized_stealths = {
            "deanonymized": {},
            "connected": {}
        }

        self._open_sources()
        self._prepare_heuristics()


    def run_heuristics(self) -> None:
        for h in self._heuristics:                  
            # give in the already deanonymized stealths and receive the new ones
            stealths = h.main(self._deanonymized_stealths)

            deanonymized = stealths["deanonymized"] if "deanonymized" in stealths else {}
            connected = stealths["connected"] if "connected" in stealths else {}
            print(f"\nThis heuristics deanonymized `{len(deanonymized)}` stealth addresses and connected `{len(connected)}` stealth addresses together.  ")

            dean_size = len(self._deanonymized_stealths["deanonymized"])
            conn_size = len(self._deanonymized_stealths["connected"])

            if len(deanonymized) > 0:
                self._deanonymized_stealths["deanonymized"] = {**self._deanonymized_stealths["deanonymized"], **deanonymized}   
            if len(connected) > 0:
                self._deanonymized_stealths["connected"] = {**self._deanonymized_stealths["connected"], **connected}

            dean_new_size = len(self._deanonymized_stealths["deanonymized"]) - dean_size
            conn_new_size = len(self._deanonymized_stealths["connected"]) - conn_size
            if dean_new_size < 0: dean_new_size = 0
            if conn_new_size < 0: conn_new_size = 0

            print(f"With this, `{dean_new_size}` new stealth addresses have been added to the deanonymization set and `{conn_new_size}` new stealth addresses have been connected together.  ")
            print(f"\n**TOTAL deanonymized stealths: `{len(self._deanonymized_stealths['deanonymized'])}/{len(self._all_stealths)}`**  ")
            print(f"**TOTAL connected stealths: `{len(self._deanonymized_stealths['connected'])}/{len(self._all_stealths)}`**")

        self._summarize_heuristics()


    def _open_sources(self) -> None:
        with open(Heuristics.data_path+"umbra_contract_txs.json", "r") as file:
            data = json.load(file)
        with open(Heuristics.data_path+"stealth_key_registry_contract_txs.json", "r") as file:
            skr_data = json.load(file)

        self._contract_txs = data["result"]
        self._skr_contract_txs = skr_data["result"]

    def _prepare_heuristics(self) -> None:

        ### common_statistics --> ###
        #2
        for d in self._contract_txs.copy():
                if d["functionName"] == fn.S_ETH.value:
                    stealth = d[d["functionName"]]["_receiver"]
                    sent_eth = int(d["value"])

                    for tx in d[d["functionName"]][stealth]:
                        # If there are more tx, then withdrawn_eth will not be equal to sent eth
                        withdrawn_eth = int(tx["value"]) + (int(tx["gasUsed"]) * int(tx["gasPrice"]))

                    if sent_eth != withdrawn_eth:
                        self._contract_txs.remove(d)
        ### common_statistics ###
               
        self._all_stealths = set()
        for d in self._contract_txs:
            # Search only for sendEth() and sendToken() bacause including withdrawToken() would be redundant.
            if d["functionName"] == fn.W_TOKEN.value:
                continue

            stealth = d[d["functionName"]]["_receiver"]
            self._all_stealths.add(stealth)

        self._heuristics = []
        self._heuristics.append(Heuristics1(copy.deepcopy(self._contract_txs), copy.deepcopy(self._skr_contract_txs)))
        self._heuristics.append(Heuristics2(copy.deepcopy(self._contract_txs), []))
        self._heuristics.append(Heuristics3(copy.deepcopy(self._contract_txs), []))
        self._heuristics.append(Heuristics4(copy.deepcopy(self._contract_txs), []))

    def _summarize_heuristics(self) -> None:
        print("\n## Summarize\n")

        print("We will merge the deanonymized stealth addresses into the connections ", end="")
        print("and then remove those connections where all of the connected stealth has the *receiver address* (the key) ", end="")
        print("as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).")
        for receiver, stealths in self._deanonymized_stealths["connected"].copy().items():
        
            same = True
            for stealth, value in stealths.items():
                if stealth in self._deanonymized_stealths["deanonymized"].keys():
                    """
                        Merge the deanonymized stealth addresses into the connections.
                    """
                    stealths[stealth] = self._deanonymized_stealths["deanonymized"][stealth]

                    if stealths[stealth]["underlying"] != receiver:
                        same = False
                else:
                    same = False

            if same:
                """
                    Remove those connections where all of the connected stealth has the receiver address (the key) as their
                    underlying address.
                """
                del self._deanonymized_stealths["connected"][receiver]


        print("\nAfter the revision, these are the final results:  ", end="")
        print(f"\n**TOTAL deanonymized stealths: `{len(self._deanonymized_stealths['deanonymized'])}/{len(self._all_stealths)}`**  ")
        print(f"**TOTAL connected stealths: `{len(self._deanonymized_stealths['connected'])}/{len(self._all_stealths)}`**  ")
        total = len(self._all_stealths) - (len(self._deanonymized_stealths['deanonymized']) + len(self._deanonymized_stealths['connected']))
        print(f"There are `{total}` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.")


        with open(access.network.value+"_results.json", "w") as file:
            json.dump(self._deanonymized_stealths, file)

        print(f"\nAll the results were printed out to **{access.network.value}_results.json** file.")


try:
    match sys.argv[1]:
        case "mainnet":
            network = Network.MAINNET
        case "polygon":
            network = Network.POLYGON
        case default:
            sys.exit("Incorrect 1. argument! (mainnet, polygon)")

except IndexError as err:
    sys.exit("Please give 1 argument! (mainnet, polygon)")

access.network = network
Heuristics.init_paths()


with open(network.value+"_output.md", "w") as file:
    sys.stdout = file

    print(f"# Umbra Deanonymization on {network.value}")

    stats = MyStatistics()
    stats.run_heuristics()
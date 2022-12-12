import sys
import json
import copy
sys.path.append("./")
sys.stdout

from helper import FunctionName as fn
from heuristics import Heuristics
from heuristics_1.heuristics_1 import Heuristics1
from heuristics_2.heuristics_2 import Heuristics2
from heuristics_3.heuristics_3 import Heuristics3
from heuristics_4.heuristics_4 import Heuristics4

class MyStatistics(object):
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self):
        super().__init__()

        self._deanonymized_stealths = {
            "confident": set(),
            "maybe": set()
        }

        self._open_sources()
        self._prepare_heuristics()

    def run_heuristics(self) -> None:
        for h in self._heuristics:                  
            # give in the already deanonymized stealths and receive the new ones
            stealths = h.main(self._deanonymized_stealths)

            confident = stealths["confident"] if "confident" in stealths else {}
            maybe = stealths["maybe"] if "maybe" in stealths else {}
            print(f"\nThis heuristics deanonymized `{len(confident)}` stealth addresses with high and `{len(maybe)}` with low certainty.  ")

            conf_size = len(self._deanonymized_stealths["confident"])
            mayb_size = len(self._deanonymized_stealths["maybe"])

            if len(confident) > 0:
                self._deanonymized_stealths["confident"] = {*self._deanonymized_stealths["confident"], *confident}   
            if len(maybe) > 0:
                self._deanonymized_stealths["maybe"] = {*self._deanonymized_stealths["maybe"], *maybe}

            conf_new_size = len(self._deanonymized_stealths["confident"]) - conf_size
            mayb_new_size = len(self._deanonymized_stealths["maybe"]) - mayb_size
            if conf_new_size < 0: conf_new_size = 0
            if mayb_new_size < 0: mayb_new_size = 0

            print(f"With this, `{conf_new_size}` new stealth addresses with high and `{mayb_new_size}` with low certainty have been added to the deanonymization set.")
            print(f"\n**TOTAL with high certainty: `{len(self._deanonymized_stealths['confident'])}/{len(self._contract_txs)}`**  ")
            print(f"**TOTAL with low certainty: `{len(self._deanonymized_stealths['maybe'])}/{len(self._contract_txs)}`**")

    def _open_sources(self) -> None:
        with open("umbra/data/mainnet/umbra_contract_txs.json", "r") as file:
            data = json.load(file)
        with open("umbra/data/mainnet/stealth_key_registry_contract_txs.json", "r") as file:
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
                    withdrawn_eth = int(tx["value"]) + (int(tx["gasUsed"]) * int(tx["gasPrice"]))
                    if sent_eth != withdrawn_eth:
                        self._contract_txs.remove(d)
        ### common_statistics ###
               

        self._heuristics = []
        self._heuristics.append(Heuristics1(copy.deepcopy(self._contract_txs), copy.deepcopy(self._skr_contract_txs)))
        self._heuristics.append(Heuristics2(copy.deepcopy(self._contract_txs), []))
        self._heuristics.append(Heuristics3(copy.deepcopy(self._contract_txs), []))
        self._heuristics.append(Heuristics4(copy.deepcopy(self._contract_txs), []))

with open("mainnet_output.md", "w") as file:
    sys.stdout = file

    print("# Umbra Deanonymization")

    stats = MyStatistics()
    stats.run_heuristics()
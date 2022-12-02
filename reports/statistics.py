import sys
import json
import copy

from helper import FunctionName as fn
from heuristics import Heuristics
from heuristics_1.heuristics_1 import Heuristics1
from heuristics_2.heuristics_2 import Heuristics2

class MyStatistics(object):
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self):
        super().__init__()

        self._deanonymized_stealths = {}

        self._open_sources()
        self._prepare_heuristics()

    def run_heuristics(self) -> None:
        for h in self._heuristics:
            stealths = h.main()

            print(f"\nThis heuristics deanonymized {len(stealths)} stealth addresses.")
            p_size = len(self._deanonymized_stealths)
            self._deanonymized_stealths = {*self._deanonymized_stealths, *stealths}
            new = len(self._deanonymized_stealths) - p_size
            if new < 0: new = 0
            print(f"With this, {new} new stealth addresses have been added to the deanonymization set.\nTOTAL: {len(self._deanonymized_stealths)}/{len(self._contract_txs)}")

    def _open_sources(self) -> None:
        with open("umbra/data/umbra_contract_txs.json", "r") as file:
            data = json.load(file)
        with open("umbra/data/stealth_key_registry_contract_txs.json", "r") as file:
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

stats = MyStatistics()
stats.run_heuristics()
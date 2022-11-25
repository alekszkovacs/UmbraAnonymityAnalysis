import sys
import json
import copy

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

        self._open_sources()
        self._prepare_heuristics()

    def run_heuristics(self) -> None:
        for h in self._heuristics:
            h.main()


    def _open_sources(self) -> None:
        with open("umbra/data/umbra_contract_txs.json", "r") as file:
            data = json.load(file)
        with open("umbra/data/stealth_key_registry_contract_txs.json", "r") as file:
            skr_data = json.load(file)

        self._contract_txs = data["result"]
        self._skr_contract_txs = skr_data["result"]

    def _prepare_heuristics(self) -> None:
        self._heuristics = []
        self._heuristics.append(Heuristics1(copy.deepcopy(self._contract_txs), copy.deepcopy(self._skr_contract_txs)))
        self._heuristics.append(Heuristics2(copy.deepcopy(self._contract_txs), []))

stats = MyStatistics()
stats.run_heuristics()
from abc import ABC, abstractmethod

class Heuristics(ABC):
    _instance = None


    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__()
        self._contract_txs = contract_txs
        self._skr_contract_txs = skr_contract_txs


    @abstractmethod
    def main(self) -> None:
        pass
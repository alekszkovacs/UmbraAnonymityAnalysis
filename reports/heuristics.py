from abc import ABC, abstractmethod

class Heuristics(ABC):
    _instance = None
    network = None

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__()
        self._contract_txs = contract_txs
        self._skr_contract_txs = skr_contract_txs

    
    def main(self, deanonymized_stealths: dict = {}) -> dict:
        self._print_intro()
        results = self._get_results()
        statistics = self._get_statistics(results)
        return self._return_stealths(statistics)


    @abstractmethod
    def _print_intro(self) -> None:
        pass

    @abstractmethod
    def _get_results(self) -> list:
        pass

    @abstractmethod
    def _get_statistics(self, results: list) -> set:
        pass

    @abstractmethod
    def _return_stealths(self, statistics) -> set:
        pass
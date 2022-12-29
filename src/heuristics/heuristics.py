from abc import ABC, abstractmethod
import json
import sys

from src.helper import Network, access


class Heuristics(ABC):
    """
        Singleton abstract class.
        The children of this class will be singletons.

        It would be more pythonic if we would implement the singleton pattern with instantiating this class once in this
        module and then import the module elsewhere, but since it's an abstract class we can't do that, so stick with
        the classic singleton pattern.
    """
    
    _instance = None
    data_path = None
    result_path = None

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__()
        self._contract_txs = contract_txs
        self._skr_contract_txs = skr_contract_txs


    @classmethod
    def init_paths(cls):
        """
            Call after initializing network
        """
        if getattr(access, "network", None) is not None:
            cls.data_path = f"data/{access.network.value}/"
            cls.result_path = f"data/{access.network.value}/results/"
        else:
            raise ValueError("Network is not yet defined.")

    
    def main(self, deanonymized_stealths: dict = {}) -> dict:
        self._deanonymized_stealths = deanonymized_stealths
        self._print_intro()
        results = self._get_results()
        statistics = self._get_statistics(results)
        return self._return_stealths(statistics)


    @abstractmethod
    def _print_intro(self) -> None:
        pass

    @abstractmethod
    def _get_results(self) -> list | dict:
        pass

    @abstractmethod
    def _get_statistics(self, results: list | dict) -> set:
        pass

    @abstractmethod
    def _return_stealths(self, statistics: set) -> dict:
        pass


def run_single_heuristics(heuristics: Heuristics) -> None:

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

    with open(Heuristics.data_path+"umbra_contract_txs.json", "r") as file:
        data = json.load(file)
    with open(Heuristics.data_path+"stealth_key_registry_contract_txs.json", "r") as file:
        skr_data = json.load(file)

    contract_txs = data["result"]
    skr_contract_txs = skr_data["result"]

    h = heuristics(contract_txs, skr_contract_txs)
    h.main()
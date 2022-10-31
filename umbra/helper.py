import os
from dotenv import load_dotenv
from web3 import Web3
from ens import ENS
from enum import Enum


class Access(object):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self):
        load_dotenv()
        self.ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
        self.WEB3_WEBSOCKET_PROVIDER = os.environ["WEB3_WEBSOCKET_PROVIDER"]

        self.w3 = Web3(Web3.WebsocketProvider(self.WEB3_WEBSOCKET_PROVIDER))
        self.ns = ENS.fromWeb3(self.w3)
        

class Argument(Enum):
    UMBRA = 1
    REGISTRY = 2
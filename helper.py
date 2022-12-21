import os
from dotenv import load_dotenv
from web3 import Web3
from ens import ENS
from enum import Enum
import time
from datetime import timedelta

class Network(Enum):
    MAINNET = "mainnet"
    POLYGON = "polygon"

class Contract(Enum):
    UMBRA = 1
    REGISTRY = 2

class FunctionName(Enum):
    S_ETH = "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)"
    S_TOKEN = "sendToken(address _receiver, address _tokenAddr, uint256 _amount, bytes32 _pkx, bytes32 _ciphertext)"
    W_TOKEN = "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)"


class Access(object):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance
   
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        load_dotenv()

    def init_network(self, network: Network) -> None:
        self.network = network
        if network == Network.MAINNET:
            self.API_ADDR = os.environ["MAINNET_API_ADDR"]
            self.API_KEY = os.environ["MAINNET_API_KEY"]

            m_http = os.environ["MAINNET_WEB3_HTTP_PROVIDER"].strip()
            m_websocket = os.environ["MAINNET_WEB3_WEBSOCKET_PROVIDER"].strip()
            if m_http != "": self.WEB3_PROVIDER = m_http
            if m_websocket != "": self.WEB3_PROVIDER = m_websocket

            self.w3 = Web3(Web3.WebsocketProvider(self.WEB3_PROVIDER))
        elif network == Network.POLYGON:
            self.API_ADDR = os.environ["POLYGON_API_ADDR"]
            self.API_KEY = os.environ["POLYGON_API_KEY"]

            # Since the found (at least that I've found) websocket provider had poor performance, and infura (which has
            # good performance) only has http for polygon, I will use http...
            m_http = os.environ["POLYGON_WEB3_HTTP_PROVIDER"].strip()
            m_websocket = os.environ["POLYGON_WEB3_WEBSOCKET_PROVIDER"].strip()
            if m_http != "": self.WEB3_PROVIDER = m_http
            if m_websocket != "": self.WEB3_PROVIDER = m_websocket
            
            self.w3 = Web3(Web3.HTTPProvider(self.WEB3_PROVIDER))

        self.ns = ENS.fromWeb3(self.w3)
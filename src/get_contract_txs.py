from web3 import Web3
from ens import ENS
from ens import exceptions
from dotenv import load_dotenv
import requests
import json
import os
import sys
import time
from datetime import timedelta
from enum import Enum
from get_ens_name import get_ens_name
from ratelimit import limits, sleep_and_retry

load_dotenv()
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
WEB3_WEBSOCKET_PROVIDER = os.environ["WEB3_WEBSOCKET_PROVIDER"]

w3 = Web3(Web3.WebsocketProvider(WEB3_WEBSOCKET_PROVIDER))
ns = ENS.fromWeb3(w3)


CALLS = 4
RATE_LIMIT = 1  # time period in seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    return requests.get(url)


class Arguments(Enum):
    UMBRA = 1
    REGISTRY = 2


get_ens_a = False
get_w_txs_a = False
ens_database = "data/ens_database.json"


try:
    match sys.argv[1]:
        case "umbra":
            fname = "data/umbra_contract_txs.json"
            contract_addr = "0xfb2dc580eed955b528407b4d36ffafe3da685401"
            input_arg = Arguments.UMBRA
        case "registry":
            fname = "data/stealth_key_registry_contract_txs.json"
            contract_addr = "0x31fe56609C65Cd0C510E7125f051D440424D38f3"
            input_arg = Arguments.REGISTRY
        case default:
            sys.exit("Incorrect 1. argument! (umbra, registry)")

    if len(sys.argv) == 3:
        if sys.argv[2] == "ens-a":
            get_ens_a = True
        elif sys.argv[2] == "w_txs-a":
            get_w_txs_a = True
        elif sys.argv[2] == "all":
            get_ens_a = True
            get_w_txs_a = True
        else:
            sys.exit("Incorrect 2. argument! (ens-a, w_txs-a, all)")

except IndexError as err:
    sys.exit("Please give an argument! (umbra, registry)")


try:
    with open(fname, "r") as file:
        og_data = json.load(file)
        # lb = int(og_data["last_block"])-10 #earlier blocks are definitely unmutable
        lb = int(og_data["last_block"]) + 1
except FileNotFoundError as err:
    og_data = {"result": []}
    lb = 0

print(f"Getting contract transactions from block {lb}...")
response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_addr}&startblock={lb}&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}")
print(f"Response code: {response.status_code}")

data_json = response.text
data = json.loads(data_json)

if int(response.status_code) == 200:
    downloaded_count = len(data["result"])
    if lb == 0:
        del data["result"][0]
        downloaded_count -= 1

    print(f"Successfully downloaded {downloaded_count} transactions.")

    try:
        if input_arg == Arguments.UMBRA:
            """
            Decode function inputs:
            """
            if downloaded_count != 0:
                contract_abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_addr}&apikey={ETHERSCAN_API_KEY}"
                contract_abi = json.loads(requests.get(contract_abi_endpoint).text)
                contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_addr), abi=contract_abi["result"])

                # If an error has stopped the previous decoding
                # So every data is decoded, not just the new ones
                if "last_decoded" in og_data: # Whether it's the first time
                    for d in reversed(og_data["result"]):
                        if d["hash"] == og_data["last_decoded"]:
                            temp_i = og_data["result"].index(d)
                            break

                    og_data["result"] = [*og_data["result"], *data["result"]]
                    contract_txs = og_data["result"][temp_i + 1 :]
                
                # If we don't have any data yet
                else:
                    contract_txs = og_data["result"] = [*data["result"]]

                # contract_txs point to the undecoded txs
                n = 0
                l = len(contract_txs)
                start = time.time()
                for d in contract_txs:
                    n += 1
                    if d["functionName"] == "":
                        now = time.time()
                        print(f"{n}/{l} record(s) decoded. Elapsed time: {timedelta(seconds=now-start)}\r", end="")
                        continue

                    func_obj, func_params = contract.decode_function_input(d["input"])

                    for key, value in func_params.items():
                        if not (isinstance(value, str) or isinstance(value, int)):
                            func_params[key] = str(value)  # it's bytes

                    d[d["functionName"]] = func_params
                    og_data["last_decoded"] = d["hash"]

                    now = time.time()
                    print(f"{n}/{l} record(s) decoded. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

                print()

            """
            Get withdraw txs:
            """
            contract_txs = og_data["result"]

            if get_w_txs_a:
                n = 0
            else:
                # it can be the first time
                if "last_withdraw" in og_data:
                    for d in reversed(contract_txs):
                        if d["hash"] == og_data["last_withdraw"]:
                            # if downloaded_count == 0 -> n = 0
                            n = contract_txs.index(d) + 1
                            break
                else: n = 0

            contract_txs = contract_txs[n:]
            l = len(contract_txs)
            start = time.time()
            found = 0
            for d in contract_txs:
                n += 1

                if d["functionName"]== "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)":
                    _address = d[d["functionName"]]["_receiver"]
                elif d["functionName"]== "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
                    _address = d[d["functionName"]]["_acceptor"]
                else:
                    continue

                if get_w_txs_a:
                    if _address in d[d["functionName"]]:
                        if len(d[d["functionName"]][_address]) == w3.eth.get_transaction_count(Web3.toChecksumAddress(_address)):
                            og_data["last_withdraw"] = d["hash"]
                            now = time.time()
                            print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")
                            continue

                response = call_api(f"https://api.etherscan.io/api?module=account&action=txlist&address={_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}")

                if response.status_code == 200:
                    data_json = response.text
                    data = json.loads(data_json)
                    d[d["functionName"]][_address] = data["result"]
                    found += len(data["result"])

                og_data["last_withdraw"] = d["hash"]
                now = time.time()
                print(f"{n}/{l} records checked for withdraw, {found} new found. Elapsed time: {timedelta(seconds=now-start)}\r", end="")


        """
        Get ens:
        """
        contract_txs = og_data["result"]

        with open(ens_database, "r") as file:
            ens_db = json.load(file)

        # Whether want to check all the addresses because of the case of latter ens registration
        if get_ens_a:
            n = 0
        else:
            #it can be the first time
            if "last_ens" in og_data:
                for d in reversed(contract_txs):
                    if d["hash"] == og_data["last_ens"]:
                        # if downloaded_count == 0 -> n = 0
                        n = contract_txs.index(d) + 1
                        break
            else: n = 0

        contract_txs = contract_txs[n:]
        l = len(contract_txs)
        _found = _local =0
        start = time.time()
        for d in contract_txs:
            n += 1
            if not (d["functionName"] == "") and not ("sender_ens" in d):
                try:
                    _res = get_ens_name(d, "from", "sender_ens", ns, ens_db)
                    if _res["r"]:
                        if _res["s"] == "net": _found += 1
                        elif _res["s"] == "db": _local += 1

                    if input_arg == Arguments.UMBRA:
                        #eth
                        if d["functionName"] == "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)":
                            k = d[d["functionName"]]["_receiver"]
                            for tx in d[d["functionName"]][k]:
                                if "receiver_ens" not in tx:
                                    _res = get_ens_name(tx, "to", "receiver_ens", ns, ens_db)
                                    if _res["r"]:
                                        if _res["s"] == "net": _found += 1
                                        elif _res["s"] == "db": _local += 1

                        #erc20-token
                        elif d["functionName"] == "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
                            if "receiver_ens" not in d[d["functionName"]]:
                                _res = get_ens_name(d[d["functionName"]], "_acceptor", "receiver_ens", ns, ens_db)
                                if _res["r"]:
                                    if _res["s"] == "net": _found += 1
                                    elif _res["s"] == "db": _local += 1
                        
                #ens.exceptions
                except exceptions.InvalidName as err:
                    print(f"Error occured at the {n}th item: {err}\nContinuing the process...")

            og_data["last_ens"] = d["hash"]
            now = time.time()
            print(f"{n}/{l} records checked against ENS, {_found} new found, {_local} gained from local db. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

        print()

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    finally:
        og_data["last_block"] = og_data["result"][-1]["blockNumber"]
        # last_decoded has been already updated for this time

        with open(fname, "w") as file:
            json.dump(og_data, file)

        trx_count = len(og_data["result"])
        print(f"{trx_count} txs have been written into the file.")

        with open(ens_database, "w") as file:
            json.dump(ens_db, file) 
else:
    sys.exit("Function was unable to download new transactions.")
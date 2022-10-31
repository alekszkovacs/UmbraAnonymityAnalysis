from helper import Access, Argument
from get_ens_name import get_ens_name

from ens import exceptions
import json
import time
from datetime import timedelta


_access = Access()
ens_database = "umbra/data/ens_database.json"

def get_txs_ens(og_data: dict, downloaded_data: list, input_arg: Argument, _all: bool) -> None:

    contract_txs = og_data["result"]

    try:
        with open(ens_database, "r") as file:
            ens_db = json.load(file)

        # Whether want to check all the addresses because of the case of latter ens registration
        if _all:
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

        contract_txs = [*contract_txs[n:], *downloaded_data]

        n = 0
        l = len(contract_txs)
        _found = _local =0
        start = time.time()

        for d in contract_txs:
            n += 1
            if not (d["functionName"] == "") and not ("sender_ens" in d):
                try:
                    _res = get_ens_name(d, "from", "sender_ens", ens_db)
                    if _res["r"]:
                        if _res["s"] == "net": _found += 1
                        elif _res["s"] == "db": _local += 1

                    if input_arg == Argument.UMBRA:
                        #eth
                        if d["functionName"] == "sendEth(address _receiver, uint256 _tollCommitment, bytes32 _pkx, bytes32 _ciphertext)":
                            k = d[d["functionName"]]["_receiver"]
                            for tx in d[d["functionName"]][k]:
                                if "receiver_ens" not in tx:
                                    _res = get_ens_name(tx, "to", "receiver_ens", ens_db)
                                    if _res["r"]:
                                        if _res["s"] == "net": _found += 1
                                        elif _res["s"] == "db": _local += 1

                        #erc20-token
                        elif d["functionName"] == "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)":
                            if "receiver_ens" not in d[d["functionName"]]:
                                _res = get_ens_name(d[d["functionName"]], "_acceptor", "receiver_ens", ens_db)
                                if _res["r"]:
                                    if _res["s"] == "net": _found += 1
                                    elif _res["s"] == "db": _local += 1
                        
                #ens.exceptions
                except exceptions.InvalidName as err:
                    print(f"Error occured at the {n}th item: {err}\nContinuing the process...")

            og_data["last_ens"] = d["hash"]
            now = time.time()
            print(f"{n}/{l} records checked against ENS, {_found} new found, {_local} gained from local db. Elapsed time: {timedelta(seconds=now-start)}\r", end="")

        if l == 0:
            print("0 record checked against ENS.")
        else:
            print()

    finally:
        with open(ens_database, "w") as file:
            json.dump(ens_db, file) 
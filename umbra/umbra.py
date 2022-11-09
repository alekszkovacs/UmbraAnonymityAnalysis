from helper import Access, Argument
from download_txs import download_txs
from decode_txs_input import decode_txs_input
from get_withdraw_txs import get_withdraw_txs
from get_txs_ens import get_txs_ens

import json
import sys


get_ens_a = False
get_w_txs_a = False


try:
    match sys.argv[1]:
        case "umbra":
            fname = "umbra/data/umbra_contract_txs.json"
            contract_addr = "0xfb2dc580eed955b528407b4d36ffafe3da685401"
            input_arg = Argument.UMBRA
        case "registry":
            fname = "umbra/data/stealth_key_registry_contract_txs.json"
            contract_addr = "0x31fe56609C65Cd0C510E7125f051D440424D38f3"
            input_arg = Argument.REGISTRY
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


downloaded_data = download_txs(contract_addr, lb)
downloaded_count = len(downloaded_data)

print(f"Successfully downloaded {downloaded_count} new transactions.")

if lb == 0:
    downloaded_data = downloaded_data[1:]

try:
    """
    We don't want to concat og_data and downloaded_data yet,
    so there is less data to check against "last_..." in the called methods.
    """
    if input_arg == Argument.UMBRA:
        decode_txs_input(contract_addr, og_data, downloaded_data)

        get_withdraw_txs(og_data, downloaded_data, get_w_txs_a)

    get_txs_ens(og_data, downloaded_data, input_arg, get_ens_a)

finally:
    og_data["result"] = [*og_data["result"], *downloaded_data]
    og_data["last_block"] = og_data["result"][-1]["blockNumber"]

    with open(fname, "w") as file:
        json.dump(og_data, file)

    trx_count = len(og_data["result"])
    print(f"{trx_count} txs have been written into the file.")
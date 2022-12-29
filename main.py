import sys
sys.dont_write_bytecode = True # Prevent the creation of __pycache__ directories

from src.helper import access, Contract, Network
from src.umbra import umbra
from src.heuristics.heuristics import Heuristics
from src.statistics import statistics

_get_ens_a = False
_get_w_txs_a = False


try:
    print("\nChoose whether you want to download transactions or want to run the heuristics! (t, h)")
    operation = ""
    while operation != "t" and operation != "h":
        operation = str(input())

    print("\nChoose the network which you want to use for the operation!")
    networks = [n.value for n in Network]
    print(networks, end="")
    print(": ", end="")
    temp = ""
    while temp not in networks:
        temp = str(input())
    for n in Network:
        if n.value == temp:
            access.network = n

    access.init_network()

    match operation:
        case "t":

            print("\nChoose the contract whose transactions you want to download!")
            contracts = [c.value for c in Contract]
            print(contracts, end="")
            print(": ", end="")
            temp = ""
            while temp not in contracts:
                temp = str(input())
            for c in Contract:
                if c.value == temp:
                    access.contract = c

            access.init_contract()

            print("\nAdditional arguments: (leave empty if you don't want to run the code in special mode)")
            print("all-ens -> if you want to download all the Umbra ENS names from block 0")
            print("all-w   -> if you want to download all the Umbra ether withdraw transactions from block 0")
            print("all     -> if you want to do both")
            temp = None
            while temp not in ["all-ens", "all-w", "all", ""]:
                temp = str(input())

            match temp:
                case "all-ens":
                    if access.network.value == Network.MAINNET:
                        _get_ens_a = True
                    else:
                        sys.exit(f"Inappropriate 3. argument. You can't use ENS names on polygon network!")
                case "all-w":
                    if contract == Contract.UMBRA:
                        _get_w_txs_a = True
                    else:
                        sys.exit(f"Inappropriate 3. argument. No need to download withdraw txs for the stealth key registry!")
                case "all":
                    if access.network.value == Network.MAINNET:
                        _get_ens_a = True
                    else:
                        sys.exit(f"Inappropriate 3. argument. You can't use ENS names on polygon network!")
                    if contract == Contract.UMBRA:
                        _get_w_txs_a = True
                    else:
                        sys.exit(f"Inappropriate 3. argument. No need to download withdraw txs for the stealth key registry!")

            fpath = f"data/{access.network.value}"
            fname = f"{access.contract.value}_contract_txs"
            umbra(f"{fpath}/{fname}.json", f"{fpath}/{fname}_BACKUP.json", _get_ens_a, _get_w_txs_a)

        case "h":
            Heuristics.init_paths()

            with open(access.network.value+"_output.md", "w") as file:
                sys.stdout = file

                print(f"# Umbra Deanonymization on {access.network.value}")

                statistics.run_heuristics()

except KeyboardInterrupt:
    print("\nmanually interrupted.\n")

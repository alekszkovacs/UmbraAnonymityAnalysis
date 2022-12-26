import sys
sys.path.append('../')

from helper import access

from web3 import Web3
from ens import ENS


def get_ens_name(d: dict, key_from: str, key_to: str, ens_db: str,) -> {bool, str}:
    """
    Arguments:
        d: source dictionary
        key_from: key which you want the ens name of
        key_to: key which under you want to save the ens name
        ens_db: instance of ens_db
    Return:
        Wheter there was new ens name found
    """
    address = d[key_from]
    if address in ens_db:
        d[key_to] = ens_db[address]
        return {"r": True, "s": "db"}
    else:
        name = access.ns.name(address)
        if Web3.toChecksumAddress(address) == access.ns.address(name):
            d[key_to] = name
            ens_db[address] = name
            return {"r": True, "s": "net"}

    return {"r": False, "s": ""}
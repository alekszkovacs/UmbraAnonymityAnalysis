from web3 import Web3
from ens import ENS

def get_ens_name(d: dict, _from: str, _to: str, ns: ENS, ens_db: str,) -> {bool, str}:
    """
    Arguments:
        d: source dictionary
        _from: key which you want the ens name of
        _to: key which under you want to save the ens name
        ns: ENS provider
        ens_db: instance of ens_db
    Return:
        Wheter there was new ens name found
    """
    address = d[_from]
    if address in ens_db:
        d[_to] = ens_db[address]
        return {"r": True, "s": "db"}
    else:
        name = ns.name(address)
        if Web3.toChecksumAddress(address) == ns.address(name):
            d[_to] = name
            ens_db[address] = name
            return {"r": True, "s": "net"}

    return {"r": False, "s": ""}
import sys
sys.path.append("./")

from reports.heuristics_1_base import Heuristics1Base

class Heuristics1(Heuristics1Base):

    def __init__(self, contract_txs: list, skr_contract_txs: list):
        super().__init__(contract_txs, skr_contract_txs)
        print(__class__.network)

    def _get_statistics(self, results: list) -> set:
        receivers = list(map(lambda v: v["receiver_address"], receivers_in_skr))
        print(f"There are `{len(receivers)}/{len(self._contract_txs)}` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.")
        c_receivers = Counter(receivers)
        print(f"This means we have assigned `{len(receivers)}` stealth addresses to `{len(dict(c_receivers))}` different addresses, ", end="")

        ens = list(filter(lambda v: "ens" in v, receivers_in_skr))
        ens = list(map(lambda v: v["ens"], ens))
        ens = Counter(ens)
        print(f"which from `{len(dict(ens))}` has ens address.")

        return results
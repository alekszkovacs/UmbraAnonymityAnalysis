import sys
sys.path.append("./")

from src.helper import Network, access

from src.heuristics.heuristics import Heuristics
from src.heuristics.heuristics_1.heuristics_1 import Heuristics1
from src.heuristics.heuristics_2.heuristics_2 import Heuristics2
from src.heuristics.heuristics_3.heuristics_3 import Heuristics3
from src.heuristics.heuristics_4.heuristics_4 import Heuristics4

import test.heuristics_1_test as h1
import test.heuristics_2_test as h2
import test.heuristics_3_test as h3
import test.heuristics_4_test as h4

access.network = Network.MAINNET

def run_single_heuristics(heuristics: Heuristics, test) -> None:
    h = heuristics(test["umbra_contract_txs"], test["skr_contract_txs"])
    return h._get_results()


def test_heuristics_1():
    assert len(run_single_heuristics(Heuristics1, h1.wrong)) == 0
    assert len(run_single_heuristics(Heuristics1, h1.good_1)) == 1
    assert len(run_single_heuristics(Heuristics1, h1.good_3)) == 3

def test_heuristics_2():
    assert len(run_single_heuristics(Heuristics2, h2.wrong)) == 0
    assert len(run_single_heuristics(Heuristics2, h2.good_1)) == 1
    assert len(run_single_heuristics(Heuristics2, h2.good_2)) == 2
    assert len(run_single_heuristics(Heuristics2, h2.good_3_with_token)) == 3

def test_heuristics_3():
    assert len(list(filter(lambda x: len(x["stealths"]) > 1, run_single_heuristics(Heuristics3, h3.wrong).values()))) == 0
    assert len(list(filter(lambda x: len(x["stealths"]) > 1, run_single_heuristics(Heuristics3, h3.good_1).values()))) == 1
    assert len(list(filter(lambda x: len(x["stealths"]) > 1, run_single_heuristics(Heuristics3, h3.good_1_2).values()))) == 1
    assert len(list(filter(lambda x: len(x["stealths"]) > 1, run_single_heuristics(Heuristics3, h3.good_2).values()))) == 2

def test_heuristics_4():
    res = run_single_heuristics(Heuristics4, h4.wrong)
    fees = []
    for fee, addresses in res.items():
        sender = False
        withdrawal = False
        for ad in addresses:
            if str(ad["type"]) == "send":
                sender = True
            if str(ad["type"]) == "withdraw":
                withdrawal = True
            if sender and withdrawal:
                fees.append(fee)
                break
    assert len(fees) == 0

    res = run_single_heuristics(Heuristics4, h4.good_1)
    fees = []
    for fee, addresses in res.items():
        sender = False
        withdrawal = False
        for ad in addresses:
            if str(ad["type"]) == "send":
                sender = True
            if str(ad["type"]) == "withdraw":
                withdrawal = True
            if sender and withdrawal:
                fees.append(fee)
                break
    assert len(fees) == 1

    res = run_single_heuristics(Heuristics4, h4.good_2_with_skr)
    fees = []
    for fee, addresses in res.items():
        sender = False
        withdrawal = False
        for ad in addresses:
            if str(ad["type"]) == "send":
                sender = True
            if str(ad["type"]) == "withdraw":
                withdrawal = True
            if sender and withdrawal:
                fees.append(fee)
                break
    assert len(fees) == 2
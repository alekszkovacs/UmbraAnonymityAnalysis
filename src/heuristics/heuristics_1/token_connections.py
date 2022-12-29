"""
    Get the hashes of the sendToken and withdrawToken txs, which are associated with the same stealth address.

    ### common_statistics --> ###
    #1
        We checked in #1 wether every stealth address has been used only once.
        
        The results are documented in #1, we act according to that. Since every stealth
        has been used only once, we have to search one receiver tx for every stealth address.
"""
import sys
import json

from src.helper import FunctionName as fn


def get_token_connections(contract_txs: list) -> dict:

    token_connections = {}

    for sender_tx in contract_txs:
        if sender_tx["functionName"] == fn.S_TOKEN.value:
            name = sender_tx["functionName"]
            stealth = sender_tx[name]["_receiver"]
            receiver_tx = list(filter(lambda st: st[st["functionName"]]["_stealthAddr"] == stealth,
                (filter(lambda t: t["functionName"] == fn.W_TOKEN.value, contract_txs))
            ))[0]["hash"]
            sender_tx = sender_tx["hash"]

            token_connections[stealth]({
                "sender_tx": sender_tx,
                "receiver_tx": receiver_tx
            })


    return token_connections
    #   "0x...sender": {
    #       "receiver_tx": "0x...receiver"
    #   }
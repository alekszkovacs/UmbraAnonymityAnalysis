"""
Get the hashes of the sendToken and withdrawToken txs, which are associated with the same stealth address.
"""
import json


with open("umbra/data/umbra_contract_txs.json", "r") as file:
    contract_txs = json.load(file)["result"]

try:
    with open("statistics/results/token_connections.json", "r") as file:
        token_connections = json.load(file)

except FileNotFoundError as err:
    token_connections = {}


n = -1
for sender_tx in contract_txs:
    n += 1
    if sender_tx["functionName"] == "sendToken(address _receiver, address _tokenAddr, uint256 _amount, bytes32 _pkx, bytes32 _ciphertext)":
        _name = sender_tx["functionName"]
        _stealth = sender_tx[_name]["_receiver"]
        receiver_tx = list(filter(lambda st: st[st["functionName"]]["_stealthAddr"] == _stealth, (filter(lambda t: t["functionName"] == "withdrawTokenOnBehalf(address _stealthAddr, address _acceptor, address _tokenAddr, address _sponsor, uint256 _sponsorFee, uint8 _v, bytes32 _r, bytes32 _s)", contract_txs))))

        _l = len(receiver_tx)
        if _l == 0:
            continue
        elif _l == 1:
            receiver_tx = receiver_tx[0]["hash"]
        elif _l > 1:
            receiver_tx = list(map(lambda t: t["hash"], receiver_tx))

        sender_tx = sender_tx["hash"]
        if _stealth in token_connections:
            if type(token_connections[_stealth]) is dict:
                if token_connections[_stealth]["sender_tx"] != sender_tx:
                    token_connections[_stealth] = [token_connections[_stealth], {"sender_tx": sender_tx, "receiver_tx": receiver_tx}]
            
            # if a stealth address is used more then once
            else:
                _same = False
                for t in token_connections[_stealth]:
                    if t["sender_tx"] == sender_tx:
                        _same = True
                if not _same:
                    token_connections[_stealth].append({"sender_tx": sender_tx, "receiver_tx": receiver_tx})

        else:
            token_connections[_stealth] = {"sender_tx": sender_tx, "receiver_tx": receiver_tx}

with open("statistics/results/token_connections.json", "w") as file:
    json.dump(token_connections, file)
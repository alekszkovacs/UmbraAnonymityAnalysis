from web3 import Web3
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
WEB3_WEBSOCKET_PROVIDER = os.environ["WEB3_WEBSOCKET_PROVIDER"]

w3 = Web3(Web3.WebsocketProvider(WEB3_WEBSOCKET_PROVIDER))
contract_address = "0xfb2dc580eed955b528407b4d36ffafe3da685401"
contract_abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
contract_abi = json.loads(requests.get(contract_abi_endpoint).text)
contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi["result"])

with open("../data/contract_txs.json", "r") as file:
    contract_txs = json.load(file)["result"] #all the transactions' details related to the umbra contract

contract_txs = contract_txs[1:]

output_dict = {}

for c in contract_txs:
    if c["functionName"] == "": continue
    if c["functionName"] not in output_dict.keys(): output_dict[c["functionName"]] = []
    
    func_obj, func_params = contract.decode_function_input(c["input"])
    print(func_obj)

    for key, value in func_params.items():
        if not (isinstance(value, str) or isinstance(value, int)): func_params[key] = str(value) #it's bytes

    temp_dict = {
        "input": c["input"]
    }
    temp_dict.update(func_params)

    for key, value in func_params.items():
        print(type(value))   

    output_dict[c["functionName"]].append(temp_dict)

with open("../data/function_inputs.json", "w") as file:
    json.dump(output_dict, file)
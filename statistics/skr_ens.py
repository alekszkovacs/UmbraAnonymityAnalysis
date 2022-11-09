skr_ens = []

for d in stealth_contract_txs:
    if "ens" in d:
        skr_ens.append(d["ens"])

with open("results/skr_ens.json", "w") as file:
    json.dump(skr_ens, file)
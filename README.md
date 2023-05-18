# Umbra Anonymity Analysis

This repository is dedicated to analyse user behaviour in the Umbra stealth address scheme.

## Download and install dependencies

### On Ubuntu

```bash
sudo apt-get update
sudo apt-get install git-all
# install python >= 3.10 version
sudo apt-get install python3
sudo apt-get install python3-venv python3-pip

git clone https://github.com/alekszkovacs/UmbraAnonymityAnalysis.git
cd UmbraAnonymityAnalysis/
pip install -r requirements.txt
cp sample.env .env
```

Now open the `sample.env` file, copy it to `.env` and give the necessary data respectively.

## Download transaction data

If you don't want to download all the transactions for all the networks (which would take more than 12 hours), feel free
to [download them from here](https://ikelte-my.sharepoint.com/:f:/g/personal/mufsgl_inf_elte_hu/Ep-qXCiAWFJFi-HQT4pnXrwBpFpH9BG1EcKWplQ1yI4BqA?e=2OS68d).

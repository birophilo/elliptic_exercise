import os
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv


load_dotenv()

WEI_TO_ETH = 0.000000000000000001
URL = "https://api.etherscan.io/api"


class ApiClient:

    def __init__(self, address: str, url: str = URL):

        self.address = address
        self.url = url
        self.api_key = os.getenv("ETHERSCAN_API_KEY")

    def get_smart_contract_name(self):
        """If address is a verified smart contract, retrieve contract name"""

        params = {
            "address": self.address,
            "apikey": self.api_key,
            "module": "contract",
            "action": "getsourcecode"
        }

        resp = requests.get(URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        return data["result"][0]["ContractName"]

    def get_address_balance(self) -> int:
        """Retrieve account balance in wei"""

        params = {
            "address": self.address,
            "apikey": self.api_key,
            "module": "account",
            "action": "balance",
            "tag": "latest",
        }

        # e.g. {'status': '1', 'message': 'OK', 'result': '316273376495586457384227'}
        resp = requests.get(URL, params=params)
        resp.raise_for_status()

        wei = int(resp.json()["result"])
        balance = wei * WEI_TO_ETH
        return balance

    def get_transactions(self):
        """Retrieve transactions for address, earliest first"""

        params = {
            "address": self.address,
            "apikey": self.api_key,
            "module": "account",
            "action": "txlist",
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": 10,
            "sort": "asc",
        }

        resp = requests.get(URL, params=params)
        resp.raise_for_status()

        return resp.json()

    def _format_tx_list(self) -> List:
        """
        Return a list of transactions, each in the format:
        [timeStamp, from, to, value]
        """
        resp = self.get_transactions()
        data = resp["result"]

        tx_items = [
            [
                # datetime string from timestamp
                f"{datetime.fromtimestamp(int(tx['timeStamp'])):%d-%m-%Y %H:%M:%S}",
                tx["from"],
                tx["to"],
                int(tx["value"]) * WEI_TO_ETH
            ] for tx in data
        ]

        return tx_items

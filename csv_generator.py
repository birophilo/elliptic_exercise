import os
import sys
from datetime import datetime
from typing import List

import pandas as pd

from api_client import ApiClient


CSV_DIR = "./csv"


class CsvGenerator:

    def __init__(self, address: str):
        self.address = address
        self.client = ApiClient(address=self.address)

    def _write_to_csv(self, data: List):
        """Create a CSV file in the desired directory"""
        df = pd.DataFrame(data)
        dt = datetime.today()
        date_string = f"{dt:%d-%m-%Y_%H.%M}"

        if not os.path.exists(CSV_DIR):
            os.mkdir(CSV_DIR)

        filename = f"{self.address[-7:]}_{date_string}.csv"
        rel_path = f"{CSV_DIR}/{filename}"

        df.to_csv(rel_path, index=False, header=False)
        print(f"Created file in {CSV_DIR} directory: '{filename}'")

    def _fetch_data_and_format_for_csv(self):
        """Fetch data using API client and arrange it in a dataframe"""

        balance = self.client.get_address_balance()
        contract_name = self.client.get_smart_contract_name()
        tx_items = self.client._format_tx_list()

        data = [
            ["Contract name", contract_name],
            ["Balance", balance, "ETH"],
            [],
            ["Timestamp", "From", "To", "Value"],
        ]

        data.extend(tx_items)
        return data

    def generate_csv_from_wallet_address(self):
        """The public method: fetch data, format it and write into CSV"""

        data = self._fetch_data_and_format_for_csv()
        self._write_to_csv(data)


if __name__ == "__main__":

    try:
        address = sys.argv[1]
    except IndexError:
        print(
            "Please supply an Ethereum address as follows: "
            "`python main.py <my_address>`"
        )
        sys.exit(1)

    csv_generator = CsvGenerator(address=address)
    csv_generator.generate_csv_from_wallet_address()

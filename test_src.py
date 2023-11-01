import json
import os

import pytest

from api_client import ApiClient
from csv_generator import CsvGenerator


ADDRESS_1 = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
ADDRESS_2 = "0xb2e2b6df59c0d281c26fe0405797544a247ebccb"


parent_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(parent_dir, "json-examples")


with open(os.path.join(fixtures_dir, "test-api-1.json")) as f1:
    TRANSACTIONS_1 = json.load(f1)

with open(os.path.join(fixtures_dir, "test-api-2.json")) as f2:
    TRANSACTIONS_2 = json.load(f2)

with open(os.path.join(fixtures_dir, "test-csv-formatted-data.json")) as f3:
    CSV_DATA = json.load(f3)


def test_api_client_can_fetch_transactions_1():
    """
    Test main API fetch. Delete confirmations from results
    as values change with time.
    """

    client = ApiClient(address=ADDRESS_1)
    data = client.get_transactions()

    for tx in data["result"]:
        del tx["confirmations"]

    for tx in TRANSACTIONS_1["result"]:
        del tx["confirmations"]

    assert data == TRANSACTIONS_1, (
        f"{json.dumps(data, indent=2)}"
        "\n DOES NOT EQUAL \n"
        f"{json.dumps(TRANSACTIONS_1, indent=2)}"
    )


def test_api_client_can_fetch_transactions_2():
    """
    Same test with named contract address
    """

    client = ApiClient(address=ADDRESS_2)
    data = client.get_transactions()

    for tx in data["result"]:
        del tx["confirmations"]

    for tx in TRANSACTIONS_2["result"]:
        del tx["confirmations"]

    assert data == TRANSACTIONS_2, (
        f"{json.dumps(data, indent=2)}"
        "\n DOES NOT EQUAL \n"
        f"{json.dumps(TRANSACTIONS_2, indent=2)}"
    )


def test_csv_generator_can_fetch_and_format_data_for_csv():

    # note: testing CSV-formatted data rather than file creation for brevity

    csv_generator = CsvGenerator(address=ADDRESS_1)
    csv_data = csv_generator._fetch_data_and_format_for_csv()

    assert csv_data == CSV_DATA

# Elliptic Crypto Address Exercise



## Installation

Python 3.10 and up recommended. For installation of multiple Python versions, Pyenv is one option.



Running from command line:

```bash
# clone the repo
$ git clone https://github.com/birophilo/elliptic_exercise

# set up virtualenv
$ cd elliptic_exercise
$ python -m venv env
$ source env/bin/activate

# install the requirements
$ pip install -r requirements.txt

# write your API key to a .env file
$ echo ETHERSCAN_API_KEY=<my_api_key> > .env

# run the script (it might take a few moments the first time due to Pandas loading time)
$ python csv_generator.py <ethereum_address>

# run tests
$ python -m pytest
```



Running in Python:

```python
from csv_generator import CsvGenerator

csv_generator = CsvGenerator(address=my_address)
csv_generator.generate_csv_from_wallet_address()
```




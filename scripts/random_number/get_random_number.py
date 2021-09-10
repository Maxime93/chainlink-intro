"""
This is after we have deployed:
brownie run scripts/price_feed/deploy_price_consumer.py --network kovan
"""

from brownie import RandomNumberConsumer, accounts, config

def request_random_number(account, random_number_contract):
    print(f"Request random number {random_number_contract.address}")
    random_number_contract.getRandomNumber({"from": account, })

def read_random_number(random_number_contract):
    number = random_number_contract.randomResult()
    print(f"Reading random number {number}")
    return number

def main():
    # Don't forget to fund the contract with LINK!
    account = accounts.add(config["wallets"]["from_key"])
    random_number_contract = RandomNumberConsumer[-1]
    # request_random_number(account, random_number_contract)
    number = read_random_number(random_number_contract)

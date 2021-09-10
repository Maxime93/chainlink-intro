import os

from brownie import (
    accounts, network, config,
    RandomNumberConsumer,
)

from web3 import Web3

DECIMALS = 18
INITIAL_VALUE = Web3.toWei(2000, "ether")

def get_account():
    if network.show_active() == 'local':
        account = accounts[0]
    elif network.show_active() == 'kovan':
        account = accounts.add(config["wallets"]["from_key"])
    return account

def main():
    print(network.show_active())
    account = get_account()
    print(account)
    if network.show_active() == 'local':
        pass
    elif network.show_active() == 'kovan':
        random_number = RandomNumberConsumer.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify", False),
        )

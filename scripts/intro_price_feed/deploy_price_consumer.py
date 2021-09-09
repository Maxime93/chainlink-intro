import os

from brownie import (
    accounts, network, config,
    PriceFeedConsumer,
    LinkToken,
    MockV3Aggregator,
    VRFCoordinatorMock,
    MockOracle,
    Contract
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


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Deployed to {link_token.address}")

    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        DECIMALS, INITIAL_VALUE, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")

    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account}
    )
    print(f"Deployed to {mock_vrf_coordinator.address}")

    print("Deploying Mock Oracle...")
    mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
    print(f"Deployed to {mock_oracle.address}")
    print("Mocks Deployed!")
    print("######################\n")

def main():
    print(network.show_active())
    account = get_account()
    print(account)
    if network.show_active() == 'local':
        print("Running on ganache..")
        print("\n######################")
        print("Since I am on my local ethereum, I need to mock some contracts that my contract will use:")
        deploy_mocks(DECIMALS, INITIAL_VALUE)
        print("######################\n")

        print("\n######################")
        print("Now I am deploying the actual price consumer contract")

        price_feed = PriceFeedConsumer.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify", False),
        )
        print(f"The current price of ETH is {price_feed.getLatestPrice()}")
    elif network.show_active() == 'kovan':
        contract_name = 'eth_usd_price_feed'

        # Address of the contract that will give us the price
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            MockV3Aggregator._name, contract_address, MockV3Aggregator.abi
        )

        print(contract)

        price_feed = PriceFeedConsumer.deploy(
            contract,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify", False),
        )

"""
This is after we have deployed:
brownie run scripts/price_feed/deploy_price_consumer.py --network kovan
"""

# from brownie import PriceFeedConsumer

# def main():
#     price_feed_contract = PriceFeedConsumer[-1]
#     print(f"Reading data from {price_feed_contract.address}")
#     data = price_feed_contract.getLatestPrice()
#     print(data)
#     roundID, price = data[0], data[1]
#     startedAt, timeStamp, answeredInRound = data[2], data[3], data[4]
#     print(f"The current price of ETH is ${price / 100000000}")

"""
# As a matter of a fact we do not even need to deploy a smart contract..
# Simply call MockV3Aggregator that is tied to the real contract deployed on Kovan
"""
from brownie import MockV3Aggregator, Contract, network, config

def main():
    pair = "uni_usd"
    contracts = {
        "uni_usd": {
            "contract_type": "uni_usd_price_feed",
            "decimals": 100000000,
            "currency": "$",
            "token": "UNI"
        }
    }
    historical = True
    contract_address = config["networks"][network.show_active()][contracts[pair]["contract_type"]]

    # This creates a contract object we can interact with using the
    # address where the contract is deployed and a
    # mock solidity file that has the same functions as the contract at the åaddress
    contract = Contract.from_abi(
        MockV3Aggregator._name, contract_address, MockV3Aggregator.abi
    )

    if not historical:
        data = contract.latestRoundData()
        print(data)
        roundID, price = data[0], data[1]
        startedAt, timeStamp, answeredInRound = data[2], data[3], data[4]
        print(f"The current price of {contracts[pair]['token']} is {contracts[pair]['currency']}{price/contracts[pair]['decimals']}")
    else:
        # Get the price at that point in time (determined by roundId)
        validRoundId = 18446744073709554130
        data = contract.getRoundData(validRoundId)
        print(data)
        roundID, price = data[0], data[1]
        startedAt, timeStamp, answeredInRound = data[2], data[3], data[4]
        print(f"The price of {contracts[pair]['token']} at {timeStamp} is {contracts[pair]['currency']}{price/contracts[pair]['decimals']}")
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.7;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract PriceFeedConsumer {

    AggregatorV3Interface internal priceFeed;

    /**
     * Network: Kovan
     * EG.
     * Aggregator: ETH/USD
     * Address: 0x9326BFA02ADD2366b30bacB125260Af641031331
     */
    constructor(address AggregatorAddress) public {
        priceFeed = AggregatorV3Interface(AggregatorAddress);
    }

    /**
     * Returns the latest price
     */
    function getLatestPrice() public view returns (uint80, int, uint, uint, uint80) {
        (
            uint80 roundID,
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return (roundID, price, startedAt, timeStamp, answeredInRound);
    }
}

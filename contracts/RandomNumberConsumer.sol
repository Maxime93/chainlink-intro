pragma solidity 0.6.7;

import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract RandomNumberConsumer is VRFConsumerBase {
    // keyHash to identify which chainlink oracle we use
    bytes32 public keyHash = 0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4;
    uint256 public fee; // fee we need to pay the oracle
    uint256 public randomResult;

    address public VRFCoordinatorAddress = 0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9;
    address public LinkTokenAddress = 0xa36085F69e2889c224210F603D836748e7dC0088;

    constructor() VRFConsumerBase(VRFCoordinatorAddress, LinkTokenAddress) public {
        fee = 0.1 * 10 ** 18; //0.1 LINK
    }

    function getRandomNumber() public returns (bytes32 requestId){
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        randomResult = randomness;
    }
}
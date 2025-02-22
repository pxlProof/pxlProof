// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HashStorage {
    // Replace single owner with mapping of owners
    mapping(address => bool) public owners;
    
    // Constructor to set the initial owner
    constructor() {
        owners[msg.sender] = true;
    }
    
    // Define the struct for our data
    struct AddressHashPair {
        address userAddress;
        string hashString;
    }
    
    // Public array to store the pairs
    AddressHashPair[] public addressHashPairs;
    
    // Modifier to check if sender is an owner
    modifier onlyOwner() {
        require(owners[msg.sender], "Only owner can call this function");
        _;
    }
    
    // Function to add new owner - only callable by existing owners
    function addOwner(address _newOwner) public onlyOwner {
        require(_newOwner != address(0), "Invalid address");
        require(!owners[_newOwner], "Address is already an owner");
        owners[_newOwner] = true;
    }
    
    // Function to check if an address is an owner
    function isOwner(address _address) public view returns (bool) {
        return owners[_address];
    }
    
    // Function to add new address-hash pair - now any owner can call
    function addAddressHashPair(address _userAddress, string memory _hashString) public onlyOwner {
        addressHashPairs.push(AddressHashPair(_userAddress, _hashString));
    }
    
    // Function to get the total number of pairs
    function getTotalPairs() public view returns (uint256) {
        return addressHashPairs.length;
    }
    
    // Function to get all stored pairs
    function getAllPairs() public view returns (AddressHashPair[] memory) {
        return addressHashPairs;
    }
}

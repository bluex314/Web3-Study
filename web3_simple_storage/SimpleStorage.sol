// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

contract SimpleStorage {
    uint256 myFavNumber;

    struct People {
        uint256 favNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public favNumberToNameMapping;

    function store(uint256 _number) public {
        myFavNumber = _number;
    }

    function retrive() public view returns (uint256) {
        return myFavNumber;
    }

    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People(_favNumber, _name));
        favNumberToNameMapping[_name] = _favNumber;
    }
}

from turtle import up
from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrive()
    expected = 0
    # Assert
    assert stored_value == expected


def test_deploy_updated_stored_value():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    transaction = simple_storage.store(6, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrive()
    expected = 6
    # Assert
    assert updated_stored_value == expected

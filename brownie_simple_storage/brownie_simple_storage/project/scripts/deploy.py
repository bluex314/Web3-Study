from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # The accounts are the accounts created by ganache, brownie will automatically invoke a local ganache
    # account = accounts[0]

    # Adding account from actual network (infura)
    account = get_account()

    print("Account address: ", account)
    # Contract Creation
    simple_storage = SimpleStorage.deploy({"from": account})
    # For call functions we dont have to give address
    stored_value = simple_storage.retrive()
    print(stored_value)

    # Updating stored value  # For transact function we have to give address
    transaction = simple_storage.store(4, {"from": account})
    # Waiting for one block
    transaction.wait(1)
    updated_stored_value = simple_storage.retrive()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()

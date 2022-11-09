from brownie import Contract, network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_BLOCKCHAINS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
DECIMAL = 8
STARTING_PRICE = 2000 * 10**8


def get_account(index=None, id=None):
    print("Active network: ", network.show_active())
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in (
        LOCAL_BLOCKCHAIN_ENVIRONMENT + FORKED_LOCAL_BLOCKCHAINS
    ):
        return accounts[0]
    return accounts.add(config["wallet"]["from_keys"])


contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        # MockV3Aggregator.len <= 0
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        print(
            f"contract name: {contract_type._name} \n contract_address: {contract_address}"
        )
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def get_address(contract_name):
    return get_contract(contract_name).address


def deploy_mocks(decimal=DECIMAL, intial_value=STARTING_PRICE):
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(decimal, intial_value, {"from": account})
    print("Mocks Deployed.")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=10 * 10**18
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund Contract!")
    return tx

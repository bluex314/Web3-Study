from brownie import OurToken, accounts
from web3 import Web3
from scripts.helpful_scripts import get_account

initial_supply = Web3.toWei(1000, "ether")

def deploy():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {"from": account})
    print(our_token.name())


def main():
    deploy()

from re import S
from brownie import SimpleStorage


def read_contract():
    # When ever we did deploy a contract it will be stored in deployments and we can read from it
    # -1 is for getting the last one in array. here i.e the latest deployment
    simple_storage = SimpleStorage[-1]
    stored_value = simple_storage.retrive()
    print(stored_value)


def main():
    read_contract()

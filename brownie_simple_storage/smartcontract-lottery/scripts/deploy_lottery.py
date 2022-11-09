import time
from scripts.helper_scripts import (
    fund_with_link,
    get_account,
    get_address,
    get_contract,
)
from brownie import Lottery, accounts, config, network


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_address("eth_usd_price_feed"),
        get_address("vrf_coordinator"),
        get_address("link_token"),
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery Deployed!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery Started...")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You Entered The Lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract (link)
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"Winner: {lottery.recentWinner()}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Loading env from .env file
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# installing solc
install_solc("0.8.0")

# Compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get byte code
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to ganache
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

# Connect to rinkby using infura api
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/11e247eb3a0d42c09985e7d97ffba7c1")
)

chain_id = 4
my_address = "0x296217fc3aAA4f1f7D516C49EE1ABDd275cC2922"
private_key = os.getenv("PRIVATE_KEY")

# -----------------------------------------------------------------------------------------------
# CONTRACTION CREATION
# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latests transaction (from nonce)
nonce = w3.eth.get_transaction_count(my_address)


# Build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

print("Deploying Contract...")
# Sign transaction using private key (then only we can send the transactoin)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)


# Send the transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Transaction finished...")

# ----------------------------------------------------------------------------------------------------
# CONTRACT CALLS
# Working with the contract
# Create the contract
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# Call : simulates caling to a function (no changes in the blockchain)
# Transact : for calling state chaing functions (can called on view functions also, but no state will change)
print("Initial stored value = ", end="")
print(simple_storage.functions.retrive().call())

# Increace the nonce by 1
nonce += 1

# Build the transaction
store_txn = simple_storage.functions.store(7).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# Sign the transaction
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=private_key)

# Send the transaction
signed_store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Updating stored value...")
signed_store_txn_receipt = w3.eth.wait_for_transaction_receipt(signed_store_txn_hash)
print("Value updated")

print("Updated stored value = ", end="")
print(simple_storage.functions.retrive().call())

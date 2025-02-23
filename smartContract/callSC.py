from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to an Ethereum node (replace with your node URL)
# For example, Infura endpoint for Ethereum mainnet or testnet
w3 = Web3(Web3.HTTPProvider(os.getenv('BASE_SEPOLIA_NODE_URL')))

# Debug: Check connection to Ethereum node
if not w3.is_connected():
    print("Error: Not connected to Ethereum node. Check BASE_SEPOLIA_NODE_URL and network connection.")
    exit(1)

# Contract details
contract_address = '0x2EAA134B34a4a7e043c162acd8E1273d84491472'
with open('abi.json') as json_file:
    contract_abi = json.load(json_file)

# Initialize contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Your private key (keep this secure and never share it!)
private_key = os.getenv('PRIVATE_KEY')
print(private_key)
account = Account.from_key(private_key)

def add_hash(hash_string: str):
    """
    Add a hash to the smart contract
    """
    try:
        # Build the transaction
        nonce = w3.eth.get_transaction_count(account.address)

        # Estimate gas
        gas_estimate = contract.functions.addHash(hash_string).estimate_gas({
            'from': account.address
        })

        transaction = contract.functions.addHash(hash_string).build_transaction({
            'from': account.address,
            'gas': gas_estimate,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction using the snake_case attribute
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction successful! Transaction hash: {tx_hash.hex()}")
        return tx_receipt

    except Exception as e:
        print(f"Error adding hash: {str(e)}")
        return None

def get_total_hashes():
    """
    Get the total number of hashes stored in the contract
    """
    try:
    total = contract.functions.getTotalHashes().call()
        print(f"Total number of hashes: {total}")
        return total
    except Exception as e:
        print(f"Error getting total hashes: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # print("hellos")
    # Example: Add a hash
    add_hash("QmExample123Hash")

    # Get total hashes
    get_total_hashes()

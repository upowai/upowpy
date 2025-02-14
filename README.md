# upowpy Library

`upowpy` is a Python library for interacting with uPow blockchain transactions, including sending funds, staking, voting, and managing nodes and validators on the blockchain.

## Installation

```bash
pip install upowpy
```

## Usage

To use the library, you will need to have an active blockchain key and appropriate addresses for transactions.

### Example Functions

Here are some of the key functions and their usage in the `upowpy` library.

#### Send Transaction

Send a specified amount to a given address.

```python
import asyncio
import upowpy as upow
import upowpy.utils as upow_utils

utils_instance = upow_utils.Utils()
utils_instance.set_node_url("https://api.upow.ai")

KEY = "hexKey"
TO = "wallet_address"
VOTE_TO = "wallet_address"
REVOKE_FROM = "wallet_address"
AMOUNT = "1"
VOTING_RANGE = "10"
WALLET = "wallet_address"
HASH = "tx_hash"

async def send_transaction():
    try:
        transaction_hash = await upow.send_transaction(utils_instance, KEY, TO, AMOUNT)
        print("Transaction hash:", transaction_hash)
    except Exception as e:
        print("Failed to send transaction:", str(e))

asyncio.run(send_transaction())
```

#### Stake and Unstake Transaction

Stake or unstake an amount on the blockchain.

```python
async def stake_transaction():
    transaction_hash = await upow.stake_transaction(utils_instance, KEY, AMOUNT)
    print("Transaction hash:", transaction_hash)

async def unstake_transaction():
    transaction_hash = await upow.unstake_transaction(utils_instance, KEY)
    print("Transaction hash:", transaction_hash)
```

#### Register and Deregister Inode

Register or deregister an inode on the blockchain.

```python
async def register_inode_transaction():
    transaction_hash = await upow.register_inode_transaction(utils_instance, KEY)
    print("Transaction hash:", transaction_hash)

async def deregister_inode_transaction():
    transaction_hash = await upow.deregister_inode_transaction(utils_instance, KEY)
    print("Transaction hash:", transaction_hash)
```

#### Register Validator

Register a validator on the blockchain.

```python
async def register_validator_transaction():
    transaction_hash = await upow.register_validator_transaction(utils_instance, KEY)
    print("Transaction hash:", transaction_hash)
```

#### Voting and Revoking

Vote for or revoke a vote for a validator using a specified range.

```python
async def vote_transaction():
    transaction_hash = await upow.vote_transaction(utils_instance, KEY, VOTING_RANGE, VOTE_TO)
    print("Transaction hash:", transaction_hash)

async def revoke_transaction():
    transaction_hash = await upow.revoke_transaction(utils_instance, KEY, REVOKE_FROM)
    print("Transaction hash:", transaction_hash)
```

#### find_balance and find_tx

Find balance using wallet_address and find tx info using tx_hash.

```python
async def find_balance(WALLET):
    try:
        transaction_hash = await upow.get_balance(utils_instance, WALLET)
        print("Balance:", transaction_hash)
    except Exception as e:
        print("Failed to find_balance:", str(e))

async def find_tx(HASH):
    try:
        transaction_hash = await upow.find_tx(utils_instance, HASH)
        print("tx:", transaction_hash)
    except Exception as e:
        print("Failed to find tx:", str(e))
```

#### address to point & point to address

you can convert address to point

```python
async def function_A(public_key):
    try:
        address = upow.publickey_to_address(public_key)
        print("address:", address)
    except Exception as e:
        print("Failed to get address:", str(e))

async def function_B(address):
    try:
        publicKey = upow.address_to_publickey(address)
        print("publicKey:", publicKey)
    except Exception as e:
        print("Failed to get publicKey:", str(e))
```

#### Create Wallet

Create a new wallet with a private key and corresponding public address.

```python
# Create a new wallet
wallet = upow.create_wallet()

# Access wallet details
private_key = wallet["private_key"]  # Hexadecimal private key
address = wallet["address"]          # Public address
raw_private_key = wallet["raw_private_key"]  # Raw private key value
```

The `create_wallet()` function returns a dictionary containing:

- `private_key`: The private key in hexadecimal format
- `address`: The public wallet address
- `raw_private_key`: The raw private key value

### Running the Code

You can run the asynchronous functions using the asyncio library.
`

```python
import asyncio

async def main():
    await send_transaction()
    # You can uncomment the below lines to perform other transactions.
    # await stake_transaction()
    # await unstake_transaction()
    # await register_inode_transaction()
    # await deregister_inode_transaction()
    # await register_validator_transaction()
    # await vote_transaction()
    # await revoke_transaction()
    # await find_balance(WALLET)
    # await find_tx(HASH)
    # await create_wallet()

asyncio.run(main())
```

## Error Handling

The `upowpy` library can raise several exceptions during its operation. Below is a list of the most common exceptions you might encounter, along with their descriptions and suggested actions to take if you encounter them:

### Transaction Errors

- **Double Spend Inside Same Transaction**: Attempt to spend the same resource more than once within a single transaction. **Action**: Ensure each output is only used once per transaction.
- **Double Spend**: Attempt to spend the same resource more than once across multiple transactions. **Action**: Verify and manage output spend status properly before initiating a transaction.

### Staking Errors

- **Already Staked**: Attempt to stake when already staked. **Action**: Check stake status before attempting to stake again.
- **Already Staked. Transaction is in Pending**: Your staking transaction is still being processed. **Action**: Wait for the transaction to complete before making another staking attempt.

### Voting Errors

- **Delegate Voting Power Bug**: There is an issue with how voting power is calculated or assigned. **Action**: Ensure the voting power calculations align with the current rules.
- **Delegate Already Have Voting Power**: Attempt to delegate voting power when it's already assigned. **Action**: Check the current voting power before assigning.
- **Delegate Doesn't Have Voting Power**: Attempt to revoke or use voting power that hasn't been delegated. **Action**: Ensure that voting power is assigned before using it.

### Validator Errors

- **Validator Already Registered**: Attempt to register as a validator when already registered. **Action**: Verify registration status before attempting to register.
- **Validator Registration Amount is Not Correct**: The amount provided for validator registration does not meet the required threshold. **Action**: Ensure the correct amount is sent for registration.

### Inode Errors

- **Already Registered as an Inode**: Attempt to register as an inode when already registered. **Action**: Verify inode registration status before attempting to register again.
- **This Address is an Active Inode. Cannot De-register**: Attempt to deregister an active inode. **Action**: Ensure the inode is inactive before attempting to deregister.

### General Errors

- **Invalid Outputs**: The outputs of a transaction are invalid. **Action**: Review and correct the outputs of your transaction.
- **We Are Not the Federal Reserve**: The input amount is less than the output amount. **Action**: Ensure that the inputs cover all outputs and transaction fees.

### Signature Errors

- **Signature Not Valid**: The transaction signature is not valid. **Action**: Ensure that the transaction is signed correctly with a valid private key.
- **Voter Signature Not Valid**: The signature for a voting action is invalid. **Action**: Verify that the voting transaction is signed correctly.

### Network Errors

- **Transaction Not Pushed**: The transaction could not be pushed to the network. **Action**: Check network status and retry the transaction.
- **URI Too Long for URL**: The URI constructed for a network request is too long. **Action**: Reduce the size of the request.

### UTXO Constraints

- **Too Many Inputs**: The number of inputs in a single transaction exceeds the maximum allowed limit.

  - **Error Message**: "You can spend max 255 inputs in a single transaction, not {number_of_inputs}"
  - **Action**: Reduce the number of inputs to 255 or fewer before attempting the transaction.

- **Too Many Outputs**: The number of outputs in a single transaction exceeds the maximum allowed limit.
  - **Error Message**: "You can have max 255 outputs in a single transaction, not {number_of_outputs}"
  - **Action**: Reduce the number of outputs to 255 or fewer before attempting the transaction.

---

import logging
import requests
from .upow_transactions.helpers import (
    sha256,
    string_to_bytes,
    point_to_string,
    string_to_point,
)
from .utils.utils import Utils
import decimal
from fastecdsa import keys
from .upow_transactions.constants import CURVE

wallet_utils: Utils = Utils()


async def push_tx(tx, wallet_utils: Utils):
    try:
        r = requests.get(
            f"{wallet_utils.NODE_URL}/push_tx", {"tx_hex": tx.hex()}, timeout=10
        )
        r.raise_for_status()
        res = r.json()
        if res["ok"]:
            transaction_hash = sha256(tx.hex())
            return None, transaction_hash
        else:
            return "Transaction not pushed", None
    except Exception as e:
        logging.error(f"Error during request to node: {e}")
        return str(e), None


async def send_transaction(
    wallet_utils: Utils, private_key_hex, recipients, amounts, message=None
):
    private_key = int(private_key_hex, 16)
    recipients_list = recipients.split(",")
    amounts_list = amounts.split(",")
    message_bytes = string_to_bytes(message) if message else None
    if (
        len(recipients_list) > 1
        and len(amounts_list) > 1
        and len(recipients_list) == len(amounts_list)
    ):
        tx = await wallet_utils.create_transaction_to_send_multiple_wallet(
            private_key, recipients_list, amounts_list, message_bytes
        )
    else:
        receiver = recipients_list[0]
        amount = amounts_list[0]
        tx = await wallet_utils.create_transaction(
            private_key, receiver, amount, message_bytes
        )
    error_message, transaction_hash = await push_tx(tx, wallet_utils)
    if transaction_hash:
        return transaction_hash
    else:
        raise Exception(error_message)


async def stake_transaction(wallet_utils: Utils, private_key_hex, amount):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_stake_transaction(private_key, amount)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def unstake_transaction(wallet_utils: Utils, private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_unstake_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def register_inode_transaction(wallet_utils: Utils, private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_inode_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def deregister_inode_transaction(wallet_utils: Utils, private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_inode_de_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def register_validator_transaction(wallet_utils: Utils, private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_validator_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def vote_transaction(
    wallet_utils: Utils, private_key_hex, voting_range, recipient
):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_voting_transaction(
            private_key, voting_range, recipient
        )
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def revoke_transaction(wallet_utils: Utils, private_key_hex, revoke_from):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_revoke_transaction(private_key, revoke_from)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def get_balance(wallet_utils, address: str):
    try:
        balance_info = wallet_utils.get_balance_info(address)
        formatted_total_balance = f"Total Balance: {balance_info[0]}"
        formatted_stake_balance = f"Staked Balance: {balance_info[2]}"

        balance_details = [formatted_total_balance, formatted_stake_balance]

        if balance_info[1] != decimal.Decimal("0"):
            formatted_pending_balance = f"Pending Incoming Balance: {balance_info[1]}"
            balance_details.append(formatted_pending_balance)

        if balance_info[3] != decimal.Decimal("0"):
            formatted_pending_stake_balance = (
                f"Pending Staked Balance: {balance_info[3]}"
            )
            balance_details.append(formatted_pending_stake_balance)

        if balance_info[4]:
            balance_details.append("Balance is syncing...")

        return "\n".join(balance_details)

    except Exception as e:
        raise


async def find_tx(wallet_utils: Utils, hash: str):
    try:
        balance_info = wallet_utils.get_tx(hash)
        return balance_info
    except Exception as e:
        raise


def publickey_to_address(pointx):
    try:
        address = point_to_string(pointx)
        return address
    except Exception as e:
        raise


def address_to_publickey(pointx):
    try:
        address = string_to_point(pointx)
        return address
    except Exception as e:
        raise


def create_wallet():
    """
    Creates a new wallet by generating a private key and deriving its public key.
    Returns a dictionary containing the private key (hex), public key (address), and raw private key.
    """
    try:
        private_key = keys.gen_private_key(CURVE)
        public_key = keys.get_public_key(private_key, CURVE)
        address = point_to_string(public_key)

        return {
            "private_key": hex(private_key),
            "address": address,
            "raw_private_key": private_key,
        }
    except Exception as e:
        raise Exception(f"Failed to create wallet: {str(e)}")

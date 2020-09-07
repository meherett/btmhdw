#!/usr/bin/env python3

from pybytom.transaction import Transaction
from pybytom.transaction.tools import find_smart_contract_utxo, find_p2wsh_utxo
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.utils import amount_converter
from pybytom.rpc import submit_transaction_raw
from pybytom.wallet import Wallet

import json

# Bytom network
NETWORK = "mainnet"  # Choose mainnet, solonet or testnet
# 12 word mnemonic seed
MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Bytom asset id
ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

# Initializing wallet
wallet = Wallet(network=NETWORK)
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=MNEMONIC)
# Derivation from path
wallet.from_path("m/44/153/1/0/1")

# Initializing transaction
unsigned_transaction = Transaction(network=NETWORK)
# Building transaction
unsigned_transaction.build_transaction(
    address=wallet.address(),
    inputs=[
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                network=NETWORK
            )
        )
    ],
    outputs=[
        control_address(
            asset=ASSET,
            amount=10_000_000,
            address="bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw",
            symbol="NEU"
        )
    ],
    fee=10_000_000,
    confirmations=1
)

print("Unsigned Transaction Fee:", unsigned_transaction.fee())
print("Unsigned Transaction Confirmations:", unsigned_transaction.confirmations())
print("Unsigned Transaction Hash:", unsigned_transaction.hash())
print("Unsigned Transaction Raw:", unsigned_transaction.raw())
print("Unsigned Transaction Json:", json.dumps(unsigned_transaction.json(), indent=4))
print("Unsigned Transaction Unsigned Datas:",
      json.dumps(unsigned_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Transaction Signatures:", json.dumps(unsigned_transaction.signatures(), indent=4))

# Singing unsigned transaction by xprivate key
signed_transaction = unsigned_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
    account=1,   # Account index, default to 1
    change=False,  # Addresses for change False(0)/True(1), default to False(0)
    address=1,  # Address index, default to 1
    path=None,  # Derivation from path, default to None
    indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"]  # Derivation from indexes, default to None
)

print("\nSigned Transaction Fee:", signed_transaction.fee())
print("Signed Transaction Confirmations:", signed_transaction.confirmations())
print("Signed Transaction Hash:", signed_transaction.hash())
print("Signed Transaction Raw:", signed_transaction.raw())
print("Signed Transaction Json:", json.dumps(signed_transaction.json(), indent=4))
print("Signed Transaction Unsigned Datas:",
      json.dumps(signed_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Transaction Signatures:", json.dumps(signed_transaction.signatures(), indent=4))

# Submitting transaction raw
# print("\nSubmitted Transaction Id:", submit_transaction_raw(
#     address=wallet.address(),
#     transaction_raw=signed_transaction.raw(),
#     signatures=signed_transaction.signatures(),
#     network=NETWORK
# ))

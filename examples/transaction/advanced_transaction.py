#!/usr/bin/env python3

from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.tools import find_smart_contract_utxo, find_p2wsh_utxo
from pybytom.transaction.actions import spend_utxo, control_address
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

# Initializing advanced transaction
unsigned_advanced_transaction = AdvancedTransaction(network=NETWORK)
# Building advanced transaction
unsigned_advanced_transaction.build_transaction(
    wallet.address(),  # address
    [
        spend_utxo(
            utxo=find_p2wsh_utxo(
                transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                network=NETWORK
            )
        )
    ],  # inputs
    [
        control_address(
            asset=ASSET,
            amount=0.1,
            address="bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw",
            symbol="BTM"
        )
    ],  # outputs
    10_000_000,  # fee
    1  # confirmations
)

print("Unsigned Advanced Transaction Fee:", unsigned_advanced_transaction.fee())
print("Unsigned Advanced Transaction Confirmations:", unsigned_advanced_transaction.confirmations())
print("Unsigned Advanced Transaction Hash:", unsigned_advanced_transaction.hash())
print("Unsigned Advanced Transaction Raw:", unsigned_advanced_transaction.raw())
print("Unsigned Advanced Transaction Json:", json.dumps(unsigned_advanced_transaction.json(), indent=4))
print("Unsigned Advanced Transaction Unsigned Datas:",
      json.dumps(unsigned_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Unsigned Advanced Transaction Signatures:", json.dumps(unsigned_advanced_transaction.signatures(), indent=4))

# Singing unsigned advanced transaction by xprivate key
signed_advanced_transaction = unsigned_advanced_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
    account=1,  # Account index, default to 1
    change=False,  # Addresses for change False(0)/True(1), default to False(0)
    address=1,  # Address index, default to 1
    path="m/44/153/1/0/1",  # Derivation from path, default to None
    indexes=None  # Derivation from indexes, default to None
)

print("\nSigned Advanced Transaction Fee:", signed_advanced_transaction.fee())
print("Signed Advanced Transaction Confirmations:", signed_advanced_transaction.confirmations())
print("Signed Advanced Transaction Hash:", signed_advanced_transaction.hash())
print("Signed Advanced Transaction Raw:", signed_advanced_transaction.raw())
print("Signed Advanced Transaction Json:", json.dumps(signed_advanced_transaction.json(), indent=4))
print("Signed Advanced Transaction Unsigned Datas:",
      json.dumps(signed_advanced_transaction.unsigned_datas(detail=False), indent=4))
print("Signed Advanced Transaction Signatures:", json.dumps(signed_advanced_transaction.signatures(), indent=4))

# Submitting advanced transaction raw
# print("\nSubmitted Advanced Transaction Id:", submit_transaction_raw(
#     address=wallet.address(),
#     transaction_raw=signed_advanced_transaction.raw(),
#     signatures=signed_advanced_transaction.signatures(),
#     network=NETWORK
# ))

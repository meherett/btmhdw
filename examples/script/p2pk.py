#!/usr/bin/env python3

from pybytom.script import (
    get_public_key_hash, get_p2pkh_program, get_p2wpkh_program, get_p2wpkh_address
)
from pybytom.wallet.tools import (
    get_program, get_address
)

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Bytom public key
PUBLIC_KEY: str = "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2"

# Get public key hash
public_key_hash = get_public_key_hash(public_key=PUBLIC_KEY)
print("Public Key Hash:", public_key_hash)
# Get Pay to Public Key Hash(P2PKH) program
p2pkh_program = get_p2pkh_program(public_key_hash=public_key_hash)
print("P2PKH Program:", p2pkh_program)
# Get Pay to Witness Public Key Hash(P2WPKH) program
p2wpkh_program = get_p2wpkh_program(public_key_hash=public_key_hash)
assert get_program(public_key=PUBLIC_KEY) == p2wpkh_program
print("P2WPKH Program:", p2wpkh_program)
# Get Pay to Witness Public Key Hash(P2WPKH) address
p2wpkh_address = get_p2wpkh_address(public_key_hash=public_key_hash, network=NETWORK, vapor=False)
assert get_address(program=get_program(public_key=PUBLIC_KEY), network=NETWORK, vapor=False) == p2wpkh_address
print("P2WPKH Address:", p2wpkh_address)
# Get Pay to Witness Public Key Hash(P2WPKH) vapor address
p2wpkh_vapor_address = get_p2wpkh_address(public_key_hash=public_key_hash, network=NETWORK, vapor=True)
assert get_address(program=get_program(public_key=PUBLIC_KEY), network=NETWORK, vapor=True) == p2wpkh_vapor_address
print("P2WPKH Vapor Address:", p2wpkh_vapor_address)

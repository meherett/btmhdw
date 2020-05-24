#!/usr/bin/env python3

from binascii import unhexlify
from hashlib import new, sha3_256

from ..libs.segwit import encode
from .builder import Builder


def get_public_key_hash(public_key: str) -> str:
    """
    Get Bytom public key hash().

    :param public_key: Bytom contract program(bytecode).
    :type public_key: str
    :return: hash -- Public key ripemd160 hash.

    >>> from pybytom.script import get_public_key_hash
    >>> get_public_key_hash("5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2")
    "875240ba66646d900c59dd20d843351c2fcbeedc"
    """

    if not isinstance(public_key, str):
        raise TypeError("invalid public key type, public_key must be string format")

    ripemd160 = new("ripemd160")
    ripemd160.update(unhexlify(public_key))
    public_hash = ripemd160.hexdigest()
    return public_hash


def get_script_hash(bytecode: str) -> str:
    """
    Get Bytom smart contract program(bytecode) script hash(SHA3_256).

    :param bytecode: Bytom contract program(bytecode).
    :type bytecode: str
    :return: hash -- Script SHA3-256 hash.

    >>> from pybytom.script import get_script_hash
    >>> get_script_hash("7baa8800c3c251547ac1")
    "e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    """

    if not isinstance(bytecode, str):
        raise TypeError("invalid bytecode type, bytecode must be string format")

    return sha3_256(unhexlify(bytecode)).hexdigest()


def get_p2wpkh_program(public_key_hash: str) -> str:
    """
    Get P2WPKH program return the segwit pay to public key hash program.

    :param public_key_hash: Bytom public key hash.
    :type public_key_hash: str
    :return: program -- Public key hash program.

    >>> from pybytom.script import get_p2wpkh_program
    >>> get_p2wpkh_program("875240ba66646d900c59dd20d843351c2fcbeedc")
    "0014875240ba66646d900c59dd20d843351c2fcbeedc"
    """

    if not isinstance(public_key_hash, str):
        raise TypeError("invalid public key hash type, public_key_hash must be string format")

    builder = Builder()
    builder.add_int(0)
    builder.add_bytes(unhexlify(public_key_hash))
    return builder.hex_digest()


def get_p2wsh_program(script_hash: str) -> str:
    """
    Get P2WSH program return the segwit pay to script hash program.

    :param script_hash: Bytom contract program(bytecode) script hash.
    :type script_hash: str
    :return: program -- Script hash program.

    >>> from pybytom.script import get_p2wsh_program
    >>> get_p2wsh_program("e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    "0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    """

    if not isinstance(script_hash, str):
        raise TypeError("invalid script hash type, script_hash must be string format")

    builder = Builder()
    builder.add_int(0)
    builder.add_bytes(unhexlify(script_hash))
    return builder.hex_digest()


def get_p2wpkh_address(public_key_hash: str, network="solonet") -> str:
    """
    Get P2WPKH program return the segwit pay to public key hash address.

    :param public_key_hash: Bytom public key hash.
    :type public_key_hash: str
    :param network: Bytom network, default to solonet.
    :type network: str
    :return: address -- Bytom pay to public key hash address.

    >>> from pybytom.script import get_p2wpkh_address
    >>> get_p2wpkh_address("875240ba66646d900c59dd20d843351c2fcbeedc")
    "bm1qsafypwnxv3keqrzem5sdsse4rshuhmku7kpnxq"
    """

    if not isinstance(public_key_hash, str):
        raise TypeError("invalid public key hash type, public_key_hash must be string format")
    if not isinstance(network, str):
        raise TypeError("invalid network type, network must be string format")

    if len(unhexlify(public_key_hash)) != 20:
        raise ValueError("invalid script hash, witness program must be 20 bytes for p2wpkh")

    if network not in "mainnet/solonet/testnet".split("/"):
        raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
    elif network == "mainnet":
        return encode("bm", 0x00, unhexlify(public_key_hash))
    elif network == "solonet":
        return encode("sm", 0x00, unhexlify(public_key_hash))
    elif network == "testnet":
        return encode("tm", 0x00, unhexlify(public_key_hash))


def get_p2wsh_address(script_hash: str, network="solonet") -> str:
    """
    Get P2WSH program return the segwit pay to script hash address.

    :param script_hash: Bytom contract program(bytecode) script hash.
    :type script_hash: str
    :param network: Bytom network, default to solonet.
    :type network: str
    :return: address -- Bytom pay to script hash address.

    >>> from pybytom.script import get_p2wsh_address
    >>> get_p2wsh_address("e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    "bm1qu3l27h360zvpjurgutwhcqsfxvdndgdh5uawhqysm7qk5089klfsrrlhez"
    """

    if not isinstance(script_hash, str):
        raise TypeError("invalid script hash type, script_hash must be string format")
    if not isinstance(network, str):
        raise TypeError("invalid network type, network must be string format")

    if len(unhexlify(script_hash)) != 32:
        raise ValueError("invalid script hash, witness program must be 32 bytes for p2wsh")

    if network not in "mainnet/solonet/testnet".split("/"):
        raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
    elif network == "mainnet":
        return encode("bm", 0x00, unhexlify(script_hash))
    elif network == "solonet":
        return encode("sm", 0x00, unhexlify(script_hash))
    elif network == "testnet":
        return encode("tm", 0x00, unhexlify(script_hash))
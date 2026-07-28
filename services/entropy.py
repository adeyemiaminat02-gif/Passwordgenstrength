"""Cryptographic entropy calculation service."""

import math
import string


def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy (in bits) for a given string."""
    if not password:
        return 0.0

    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += 32
    if any(c not in string.printable for c in password):
        pool_size += 32

    if pool_size == 0:
        return 0.0

    return round(len(password) * math.log2(pool_size), 2)

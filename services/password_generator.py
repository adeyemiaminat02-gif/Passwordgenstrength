"""Secure password generation module utilizing Python's secrets module."""

import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_numbers: bool = True,
    use_symbols: bool = True,
    exclude_similar: bool = False,
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a cryptographically secure random password based on custom criteria."""
    length = max(8, min(128, length))

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if exclude_similar:
        uppercase = uppercase.translate(str.maketrans("", "", "IO"))
        lowercase = lowercase.translate(str.maketrans("", "", "l"))
        digits = digits.translate(str.maketrans("", "", "01"))

    if exclude_ambiguous:
        symbols = symbols.translate(str.maketrans("", "", "{}[]()/\\'\"`~,;:.<>"))

    char_pools = []
    if use_lowercase and lowercase:
        char_pools.append(lowercase)
    if use_uppercase and uppercase:
        char_pools.append(uppercase)
    if use_numbers and digits:
        char_pools.append(digits)
    if use_symbols and symbols:
        char_pools.append(symbols)

    if not char_pools:
        char_pools = [string.ascii_lowercase, string.digits]

    # Ensure at least one character from each selected pool is present
    password_chars = [secrets.choice(pool) for pool in char_pools]

    all_chars = "".join(char_pools)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    # Securely shuffle using Fisher-Yates backed by secrets
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def generate_multiple_passwords(count: int = 5, **kwargs) -> list[str]:
    """Generate a list of secure passwords."""
    count = max(1, min(10, count))
    return [generate_password(**kwargs) for _ in range(count)]

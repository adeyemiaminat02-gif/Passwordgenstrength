"""Security recommendations and best practices dataset."""

SECURITY_TIPS = [
    "🔑 **Use Unique Passwords**: Never reuse the same password across multiple accounts. If one service is breached, all your accounts become vulnerable.",
    "🛡️ **Enable Two-Factor Authentication (2FA)**: Always enable 2FA (preferably via an Authenticator App or FIDO Key) to add an extra layer of defense.",
    "🧠 **Adopt Passphrases**: Use long passphrases made of 4+ random words (e.g., `correct-horse-battery-staple`). They are easier to remember and extremely hard to crack.",
    "📦 **Use a Dedicated Password Manager**: Use trustworthy password managers like Bitwarden, 1Password, or KeePassXC to generate and securely store complex credentials.",
    "🚫 **Avoid Personal Information**: Never include your birthday, pet's name, or phone number in passwords—attackers easily find this on social media.",
    "⚠️ **Watch Out for Phishing**: Always verify the website URL in your browser address bar before entering your password.",
]


def get_random_tips(count: int = 3) -> list[str]:
    """Return a random selection of security tips."""
    import secrets
    return secrets.SystemRandom().sample(SECURITY_TIPS, min(count, len(SECURITY_TIPS)))

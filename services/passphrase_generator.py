"""Cryptographically secure EFF passphrase generator module."""

import secrets

WORDLIST = [
    "ability", "account", "accurate", "actor", "adapter", "advanced", "advisor",
    "airline", "airport", "album", "alert", "algebra", "alien", "alpha", "alps",
    "amber", "anchor", "ancient", "angel", "angle", "animal", "anthem", "aperture",
    "apollo", "apple", "apron", "arcadia", "arch", "arctic", "arena", "arrow",
    "artist", "aspen", "asset", "atlas", "atom", "atrium", "aura", "aurora",
    "autumn", "avatar", "avenu", "aviation", "avocado", "axis", "aztec", "badge",
    "bagel", "baker", "balance", "balcony", "bamboo", "banana", "banner", "beacon",
    "beetle", "bison", "blazer", "blossom", "boulder", "breeze", "bridge", "cactus",
    "canyon", "canvas", "capital", "capsule", "carbon", "castle", "cedar", "celestial",
    "cement", "center", "chain", "chalet", "champion", "channel", "chapter", "chariot",
    "cinema", "circle", "citrus", "clover", "cobalt", "coffee", "comet", "compass",
    "copper", "coral", "cosmos", "crater", "crystal", "delta", "desert", "diamond",
    "dolphin", "dragon", "eagle", "echo", "eclipse", "emerald", "falcon", "fossil",
    "galaxy", "glacier", "granite", "harbor", "horizon", "island", "jaguar", "jungle",
    "jupiter", "lagoon", "lantern", "legend", "leopard", "liberty", "lotus", "lunar",
    "magnet", "marble", "meadow", "meteor", "monarch", "mountain", "nebula", "nectar",
    "neptune", "oasis", "ocean", "octave", "olympus", "onyx", "opal", "orchid",
    "orion", "osprey", "palace", "panther", "parrot", "phoenix", "planet", "plasma",
    "polar", "prism", "pyramid", "quartz", "radar", "radius", "redwood", "ripple",
    "safari", "sahara", "salmon", "sapphire", "saturn", "shadow", "sierra", "signal",
    "silver", "solar", "sphere", "spire", "summit", "sunflower", "sunset", "thunder",
    "timber", "titan", "topaz", "torpedo", "transit", "tropic", "tundra", "twilight",
    "typhoon", "valley", "velvet", "venture", "vessel", "vortex", "walnut", "wave",
    "whisper", "wildcat", "willow", "zenith", "zodiac"
]


def generate_passphrase(
    num_words: int = 4,
    separator: str = "-",
    include_number: bool = True,
    include_symbol: bool = False,
) -> str:
    """Generate a memorable and cryptographically strong passphrase."""
    num_words = max(3, min(10, num_words))
    selected_words = [secrets.choice(WORDLIST) for _ in range(num_words)]

    if include_number:
        rand_idx = secrets.randbelow(len(selected_words))
        selected_words[rand_idx] += str(secrets.randbelow(90) + 10)

    if include_symbol:
        symbols = "!@#$%^&*"
        rand_idx = secrets.randbelow(len(selected_words))
        selected_words[rand_idx] += secrets.choice(symbols)

    return separator.join(selected_words)

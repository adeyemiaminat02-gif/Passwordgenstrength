"""Comprehensive password strength evaluation service."""

from typing import Any, Dict
from zxcvbn import zxcvbn
from services.entropy import calculate_entropy


def analyze_password(password: str) -> Dict[str, Any]:
    """Analyze a given password returning strength metric scores and feedback."""
    if not password:
        return {
            "score": 0,
            "rating": "Very Weak",
            "entropy": 0.0,
            "crack_time": "Instant",
            "recommendations": ["Password cannot be empty."],
            "checks": {},
        }

    analysis = zxcvbn(password)

    score = analysis["score"]
    ratings = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}
    rating = ratings.get(score, "Very Weak")

    entropy = calculate_entropy(password)
    if entropy >= 80 and score >= 3:
        rating = "Very Strong"

    numerical_score = min(100, int((score / 4) * 70 + (min(entropy, 100) / 100) * 30))

    crack_time = analysis["crack_times_display"]["offline_slow_hashing_1e4_per_s"]

    # Structural composition details
    checks = {
        "length": len(password),
        "has_uppercase": any(c.isupper() for c in password),
        "has_lowercase": any(c.islower() for c in password),
        "has_numbers": any(c.isdigit() for c in password),
        "has_symbols": any(not c.isalnum() for c in password),
    }

    # Derive actionable security feedback
    recommendations = []
    feedback = analysis.get("feedback", {})

    if feedback.get("warning"):
        recommendations.append(feedback["warning"])

    for suggestion in feedback.get("suggestions", []):
        recommendations.append(suggestion)

    if len(password) < 12:
        recommendations.append("Increase length to at least 12–16 characters.")
    if not checks["has_symbols"] or not checks["has_numbers"]:
        recommendations.append("Mix numbers, symbols, and uppercase letters.")

    if not recommendations:
        recommendations.append("Great job! This password is exceptionally strong.")

    return {
        "score": score,
        "numerical_score": numerical_score,
        "rating": rating,
        "entropy": entropy,
        "crack_time": str(crack_time),
        "recommendations": recommendations,
        "checks": checks,
    }

# @Passwordgenstrengthbot 🔒

A production-ready, zero-knowledge Telegram Password Generator and Password Strength Checker Bot built with Python 3.12+ and `python-telegram-bot` v22+.

## Features

- 🎲 **Secure Password Generator**: Generates cryptographically secure passwords using Python's `secrets` module.
- 📝 **Passphrase Generator**: Generates human-friendly, high-entropy word combinations.
- 📊 **Strength Checker**: Evaluates passwords locally using `zxcvbn` dictionary and pattern matching.
- ⚙️ **User Preferences**: Persists generator settings with SQLite/PostgreSQL support using SQLAlchemy.
- 🛡️ **Strict Privacy**: Zero password logging or persistence.

---

## Local Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/Passwordgenstrengthbot.git](https://github.com/your-username/Passwordgenstrengthbot.git)
   cd Passwordgenstrengthbot

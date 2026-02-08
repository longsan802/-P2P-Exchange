import os

# Bot Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8500717921:AAEaBkRtmrUZFJ0Cd4HFI0_spzN8yr0sdZ8")
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "8057226500").split(",")]

# Webhook Configuration
WEBHOOK_ENABLED = os.environ.get("WEBHOOK_ENABLED", "False").lower() == "true"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-domain.com/webhook")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "your_webhook_secret_token")

# Webhook SSL Certificate (use Render's certificate)
SSL_CERT_PATH = os.environ.get("SSL_CERT_PATH", "cert.pem")
SSL_PRIVKEY_PATH = os.environ.get("SSL_PRIVKEY_PATH", "privkey.pem")

# Webhook Server Settings
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("PORT", "8443"))

# USDT TRC20 Wallet
USDT_WALLET = os.environ.get("USDT_WALLET", "TPtKtKZH8oQiYkbwqgYxmeEBn5ZTTSKW8A")

# Exchange Rate Settings (base rate, admin can adjust)
EXCHANGE_RATE = float(os.environ.get("EXCHANGE_RATE", "4100"))
FEE_PERCENTAGE = float(os.environ.get("FEE_PERCENTAGE", "1.0"))

# Supported Languages
LANGUAGES = {
    'en': 'English',
    'km': 'Khmer',
    'zh': '中文'
}

# Database
DATABASE_PATH = os.environ.get("DATABASE_PATH", "exchange_bot.db")

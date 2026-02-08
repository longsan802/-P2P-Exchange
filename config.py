# Bot Configuration
BOT_TOKEN = "8500717921:AAEaBkRtmrUZFJ0Cd4HFI0_spzN8yr0sdZ8"
ADMIN_IDS = [8057226500]  # Replace with actual admin Telegram user IDs

# Webhook Configuration
WEBHOOK_ENABLED = False  # Set to True when you have a public domain
WEBHOOK_URL = "https://your-domain.com:8443/webhook"  # Replace with your public URL
WEBHOOK_SECRET = "your_webhook_secret_token"  # Optional: secret token for webhook verification

# Webhook SSL Certificate (self-signed or real path)
SSL_CERT_PATH = "cert.pem"  # Path to your SSL certificate
SSL_PRIVKEY_PATH = "privkey.pem"  # Path to your SSL private key

# Webhook Server Settings
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8443

# USDT TRC20 Wallet
USDT_WALLET = "TPtKtKZH8oQiYkbwqgYxmeEBn5ZTTSKW8A"

# Exchange Rate Settings (base rate, admin can adjust)
EXCHANGE_RATE = 4100  # 1 USD = 4100 KHR (default rate, will be dynamic in production)
FEE_PERCENTAGE = 1.0  # 1% fee

# Supported Languages
LANGUAGES = {
    'en': 'English',
    'km': 'Khmer',
    'zh': '中文'
}

# Database
DATABASE_PATH = "exchange_bot.db"

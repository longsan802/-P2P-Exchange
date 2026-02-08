import requests

TOKEN = "8500717921:AAEaBkRtmrUZFJ0Cd4HFI0_spzN8yr0sdZ8"

# Delete webhook
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
r = requests.get(url)
print(f"Delete webhook: {r.json()}")

# Get bot info
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
r = requests.get(url)
print(f"Bot info: {r.json()}")

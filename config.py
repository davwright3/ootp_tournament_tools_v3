import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
BROADCASTER_ID = os.getenv("TWITCH_BROADCASTER_ID")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI", "http://localhost:3000")
REDIRECT_PORT = int(os.getenv("TWITCH_REDIRECT_PORT", "3000"))
SCOPES = os.getenv("TWITCH_SCOPES", "user:read:subscriptions")

print('Running config')

if not CLIENT_ID:
    raise ValueError("Missing TWITCH_CLIENT_ID in environment / .env file")
if not BROADCASTER_ID:
    raise ValueError("Missing TWITCH_BROADCASTER_ID in environment / .env file")
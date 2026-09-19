import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials from https://my.telegram.org
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")

# Pyrogram / Pyrofork String Session
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# MongoDB connection URI
MONGO_URL = os.environ.get("MONGO_URL", "")

# Command prefixes (default: . and !)
PREFIXES = os.environ.get("PREFIXES", ". !").split()

# Yuki API for YouTube audio/video streaming and download
MEOW_API_URL = os.environ.get("MEOW_API_URL", "https://music.yukiapi.site")
MEOW_API_KEY = os.environ.get("MEOW_API_KEY", "yuki_28d18045448fe0df857d31dfe08fcdef")

# Default delay for raids and actions (in seconds)
DEFAULT_DELAY = float(os.environ.get("DEFAULT_DELAY", "0.5"))

# Bot Branding & Version
BOT_NAME = "Premium Userbot"
BOT_VERSION = "2.0.0"

# Downloads directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

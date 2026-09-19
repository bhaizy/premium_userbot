import sys
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
import os
import sys
import glob
import asyncio
import logging
import importlib
from pyrogram import idle
from core.client import app
from core.database import init_db
from core.call_client import start_call_client
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
LOGGER = logging.getLogger("Main")

BANNER = r"""
  ____                            _                     
 |  _ \ _ __ ___ _ __ ___  _   _ | |_ ___  ___   _   _  
 | |_) | '__/ _ \ '_  _ \| | | || __/ _ \/ __| | | | | 
 |  __/| | |  __/ | | | | | |_| || || (_) \__ \ | |_| | 
 |_|   |_|  \___|_| |_| |_|\__,_| \__\___/|___/  \__,_| 
                                                        
           亗 PREMIUM TELEGRAM USERBOT v2.0 亗
"""

def load_all_modules():
    path = os.path.join(os.path.dirname(__file__), "modules", "*.py")
    files = glob.glob(path)
    count = 0
    for file in files:
        if file.endswith("__init__.py"):
            continue
        module_name = "modules." + os.path.basename(file)[:-3]
        try:
            importlib.import_module(module_name)
            count += 1
            LOGGER.info(f"Loaded module: {module_name}")
        except Exception as e:
            LOGGER.error(f"Failed to load module {module_name}: {e}", exc_info=True)
    return count


async def main():
    print(BANNER)
    LOGGER.info("Starting Premium Userbot...")

    # 1. Initialize MongoDB and cache
    await init_db()

    # 2. Dynamically import modules
    loaded_count = load_all_modules()
    LOGGER.info(f"Total modules loaded: {loaded_count}")

    # 3. Start Pyrogram / Pyrofork Client
    await app.start()
    me = await app.get_me()
    LOGGER.info(f"Userbot logged in as: {me.first_name} (@{me.username or 'No Username'}) [ID: {me.id}]")

    # 4. Start PyTgCalls client
    await start_call_client()

    # 5. Send startup confirmation to Saved Messages
    try:
        await app.send_message(
            "me",
            f"亗 **ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀʙᴏᴛ ɪꜱ ᴏɴʟɪɴᴇ** ⚡\n\n"
            f"├─ **Owner:** {me.first_name}\n"
            f"├─ **Prefixes:** {' '.join(config.PREFIXES)}\n"
            f"├─ **Modules:** {loaded_count}\n"
            f"├─ **Database:** {'Connected' if config.MONGO_URL else 'In-Memory'}\n"
            f"└─ **Yuki API:** Active 🎵\n\n"
            f"Type .help in any chat to view commands!"
        )
    except Exception as e:
        LOGGER.warning(f"Could not send startup message to Saved Messages: {e}")

    LOGGER.info("Userbot is fully ready and listening for commands!")
    await idle()
    await app.stop()
    LOGGER.info("Userbot stopped.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

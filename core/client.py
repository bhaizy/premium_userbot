import time
import logging
from pyrogram import Client, filters
import config

LOGGER = logging.getLogger("Userbot")
START_TIME = time.time()

# Initialize Pyrofork Client
if not config.STRING_SESSION:
    LOGGER.warning("STRING_SESSION is empty! Please generate one using 'python generate_session.py'")

app = Client(
    name="premium_userbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
    in_memory=True
)


def on_cmd(commands, **kwargs):
    """
    Decorator for userbot commands.
    Ensures commands only respond to the account owner (filters.me)
    using the prefixes defined in config.py (e.g., '.' and '!').
    """
    if isinstance(commands, str):
        commands = [commands]

    def decorator(func):
        @app.on_message(filters.me & filters.command(commands, prefixes=config.PREFIXES), **kwargs)
        async def wrapper(client, message):
            try:
                await func(client, message)
            except Exception as e:
                LOGGER.error(f"Error in command '{commands}': {e}", exc_info=True)
                try:
                    await message.edit_text(f"❌ **Error:** {e}")
                except Exception:
                    pass
        return wrapper
    return decorator

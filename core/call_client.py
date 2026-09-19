import logging
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from core.client import app

LOGGER = logging.getLogger("VoiceChat")

call_py = PyTgCalls(app)
ACTIVE_CALLS = set()


async def start_call_client():
    try:
        await call_py.start()
        LOGGER.info("PyTgCalls client initialized!")
    except Exception as e:
        LOGGER.warning(f"PyTgCalls start notice (may start upon first call): {e}")


async def play_audio_stream(chat_id: int, audio_path: str) -> bool:
    chat_id = int(chat_id)
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(audio_path)
        )
        ACTIVE_CALLS.add(chat_id)
        return True
    except Exception as e:
        err_msg = str(e).lower()
        if "already" in err_msg or "active" in err_msg:
            try:
                await call_py.change_stream(chat_id, AudioPiped(audio_path))
                ACTIVE_CALLS.add(chat_id)
                return True
            except Exception as e2:
                LOGGER.error(f"Failed to change stream: {e2}")
                return False
        LOGGER.error(f"Error joining voice call: {e}")
        return False


async def leave_call(chat_id: int) -> bool:
    chat_id = int(chat_id)
    try:
        await call_py.leave_group_call(chat_id)
        ACTIVE_CALLS.discard(chat_id)
        return True
    except Exception as e:
        LOGGER.error(f"Error leaving voice call: {e}")
        return False

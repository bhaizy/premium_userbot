import logging
from motor.motor_asyncio import AsyncIOMotorClient
import config

LOGGER = logging.getLogger("Database")

# In-memory caches for 0.001ms fast lookups
GMUTE_SET = set()
REPLY_RAID_SET = set()
CURRENT_DELAY = config.DEFAULT_DELAY

_client = None
_db = None


async def init_db():
    global _client, _db, CURRENT_DELAY
    if not config.MONGO_URL:
        LOGGER.warning("MONGO_URL not set! Running with in-memory storage (data will reset on restart).")
        return

    try:
        _client = AsyncIOMotorClient(config.MONGO_URL)
        _db = _client["premium_userbot"]
        
        # Load GMUTE list
        async for doc in _db.gmute.find():
            if "user_id" in doc:
                GMUTE_SET.add(int(doc["user_id"]))

        # Load REPLY_RAID list
        async for doc in _db.reply_raid.find():
            if "user_id" in doc:
                REPLY_RAID_SET.add(int(doc["user_id"]))

        # Load settings (delay)
        setting = await _db.settings.find_one({"key": "delay"})
        if setting and "value" in setting:
            CURRENT_DELAY = float(setting["value"])

        LOGGER.info(f"MongoDB connected! Loaded {len(GMUTE_SET)} gmuted users, {len(REPLY_RAID_SET)} reply-raid users.")
    except Exception as e:
        LOGGER.error(f"Failed to connect to MongoDB: {e}. Falling back to in-memory mode.")


# Gmute functions
async def add_gmute(user_id: int):
    user_id = int(user_id)
    GMUTE_SET.add(user_id)
    if _db is not None:
        try:
            await _db.gmute.update_one({"user_id": user_id}, {"": {"user_id": user_id}}, upsert=True)
        except Exception as e:
            LOGGER.error(f"DB Error add_gmute: {e}")


async def remove_gmute(user_id: int):
    user_id = int(user_id)
    GMUTE_SET.discard(user_id)
    if _db is not None:
        try:
            await _db.gmute.delete_one({"user_id": user_id})
        except Exception as e:
            LOGGER.error(f"DB Error remove_gmute: {e}")


def is_gmuted(user_id: int) -> bool:
    return int(user_id) in GMUTE_SET


def get_gmutes() -> list:
    return list(GMUTE_SET)


# Reply Raid functions
async def add_reply_raid(user_id: int):
    user_id = int(user_id)
    REPLY_RAID_SET.add(user_id)
    if _db is not None:
        try:
            await _db.reply_raid.update_one({"user_id": user_id}, {"": {"user_id": user_id}}, upsert=True)
        except Exception as e:
            LOGGER.error(f"DB Error add_reply_raid: {e}")


async def remove_reply_raid(user_id: int):
    user_id = int(user_id)
    REPLY_RAID_SET.discard(user_id)
    if _db is not None:
        try:
            await _db.reply_raid.delete_one({"user_id": user_id})
        except Exception as e:
            LOGGER.error(f"DB Error remove_reply_raid: {e}")


def is_reply_raid(user_id: int) -> bool:
    return int(user_id) in REPLY_RAID_SET


def get_reply_raids() -> list:
    return list(REPLY_RAID_SET)


# Delay functions
async def set_delay(val: float):
    global CURRENT_DELAY
    CURRENT_DELAY = float(val)
    if _db is not None:
        try:
            await _db.settings.update_one({"key": "delay"}, {"": {"value": CURRENT_DELAY}}, upsert=True)
        except Exception as e:
            LOGGER.error(f"DB Error set_delay: {e}")


def get_delay() -> float:
    return CURRENT_DELAY

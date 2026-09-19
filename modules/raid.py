import asyncio
import random
from pyrogram import Client, filters
from core.client import app, on_cmd
from core.database import (
    add_reply_raid, remove_reply_raid, is_reply_raid, 
    get_delay, set_delay
)
from helpers.ui import to_small_caps

ROASTS = [
    "Aukat me rehna seekh le beta.",
    "Jitna tera dimag hai utna to humara backup database hai.",
    "Apne baap ko mat sikha, chup chap nikal.",
    "Keyboard warrior banne se gunda nahi bante.",
    "Kyu itni bezzati karwane ka shauq hai tujhe?",
    "Tere jaise 10 roz mere blocklist me aate hain.",
    "Bolna kam kar, shakal waise bhi kharab hai teri.",
    "Kahan se aate hain ye log? Thoda dhang se baat kar.",
    "Ghar pe bolte nahi sunta, yahan bakwaas pel raha hai.",
    "Lagta hai system reboot maang raha hai tera dimag."
]

@on_cmd(["delay"])
async def delay_handler(client, message):
    args = message.text.split()
    if len(args) < 2:
        curr = get_delay()
        return await message.edit_text(f"⏱️ **Current Raid Delay:** {curr}s\nUsage: .delay <seconds>")
    try:
        val = float(args[1])
        if val < 0.1:
            return await message.edit_text("⚠️ **Minimum delay is 0.1s** to prevent Telegram FloodWait.")
        await set_delay(val)
        await message.edit_text(f"✅ **Raid Delay updated to:** {val}s")
    except ValueError:
        await message.edit_text("❌ **Invalid delay value! Please provide a number (e.g. .delay 0.5)**")


@on_cmd(["raid"])
async def raid_handler(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.edit_text("ℹ️ **Usage:** .raid <count> <message>\nExample: .raid 5 Kahan bhag gaya")

    try:
        count = int(args[1])
    except ValueError:
        return await message.edit_text("❌ **Count must be an integer!**")

    raid_text = args[2]
    await message.delete()

    delay = get_delay()
    for _ in range(count):
        try:
            await client.send_message(message.chat.id, raid_text)
            await asyncio.sleep(delay)
        except Exception:
            await asyncio.sleep(1)


@on_cmd(["rd", "replyraid"])
async def reply_raid_handler(client, message):
    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.first_name
    else:
        args = message.text.split()
        if len(args) > 1:
            try:
                user_id = int(args[1])
                name = str(user_id)
            except ValueError:
                return await message.edit_text("❌ **Provide a valid User ID or reply to a user's message.**")

    if not user_id:
        return await message.edit_text("ℹ️ **Reply to a user's message** to start Reply Raid on them.")

    await add_reply_raid(user_id)
    await message.edit_text(f"🔥 **Reply Raid Activated on:** {name} ({user_id})\n_Every message from them will be countered!_")


@on_cmd(["rrd", "dreplyraid"])
async def stop_reply_raid_handler(client, message):
    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    else:
        args = message.text.split()
        if len(args) > 1:
            try:
                user_id = int(args[1])
            except ValueError:
                return await message.edit_text("❌ **Provide a valid User ID or reply to a user's message.**")

    if not user_id:
        return await message.edit_text("ℹ️ **Reply to a user's message** to stop Reply Raid on them.")

    await remove_reply_raid(user_id)
    await message.edit_text(f"✅ **Reply Raid Deactivated for User:** {user_id}")


# Background Listener for Reply Raid
@app.on_message(~filters.me & filters.incoming, group=1)
async def incoming_reply_raid_listener(client, message):
    if not message.from_user:
        return

    if is_reply_raid(message.from_user.id):
        roast = random.choice(ROASTS)
        delay = get_delay()
        await asyncio.sleep(delay)
        try:
            await message.reply_text(roast)
        except Exception:
            pass

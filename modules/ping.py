import time
import psutil
from pyrogram import Client, filters
from core.client import on_cmd, START_TIME
from helpers.ui import format_card, format_uptime, to_small_caps
import config

@on_cmd(["ping", "p"])
async def ping_handler(client, message):
    start = time.time()
    await message.edit_text("⚡ `[ ᴘɪɴɢɪɴɢ... ]`")
    latency = round((time.time() - start) * 1000, 2)
    uptime = format_uptime(time.time() - START_TIME)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    card = format_card(
        "premium userbot",
        [
            ("latency", f"{latency} ms"),
            ("uptime", uptime),
            ("cpu usage", f"{cpu}%"),
            ("ram usage", f"{ram}%"),
            ("version", config.BOT_VERSION)
        ],
        footer="Status: Operational"
    )
    await message.edit_text(card)


@on_cmd(["pong"])
async def pong_handler(client, message):
    await message.edit_text(f"亗 **{to_small_caps('pong')}** : `0.001 ms` ⚡")


@on_cmd(["alive"])
async def alive_handler(client, message):
    me = await client.get_me()
    uptime = format_uptime(time.time() - START_TIME)
    card = format_card(
        "system status",
        [
            ("owner", f"@{me.username}" if me.username else me.first_name),
            ("uptime", uptime),
            ("engine", "Pyrofork + PyTgCalls"),
            ("database", "MongoDB Atlas (Cached)"),
            ("music api", "Yuki API (Active)")
        ],
        footer="Bot is running smoothly."
    )
    await message.edit_text(card)
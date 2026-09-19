import os
from pyrogram import Client, filters
from core.client import on_cmd
from core.call_client import play_audio_stream, leave_call
from helpers.youtube import search_youtube, download_song
from helpers.ui import format_card, format_duration, to_small_caps

@on_cmd(["vc"])
async def vc_handler(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.edit_text("ℹ️ **Usage:** .vc join or .vc leave")

    action = args[1].lower()
    chat_id = message.chat.id

    if action == "join":
        await message.edit_text("🔄 **Joining Voice Chat...**")
        # Try joining with silence or empty stream
        res = await play_audio_stream(chat_id, "resources/silence.mp3" if os.path.exists("resources/silence.mp3") else "")
        if res:
            await message.edit_text("✅ **Successfully joined Voice Chat.**")
        else:
            await message.edit_text("❌ **Could not join VC.** Make sure Voice Chat is started in this group.")

    elif action == "leave":
        await message.edit_text("🔄 **Leaving Voice Chat...**")
        res = await leave_call(chat_id)
        if res:
            await message.edit_text("🚪 **Left Voice Chat successfully.**")
        else:
            await message.edit_text("❌ **Not in Voice Chat or failed to leave.**")


@on_cmd(["play", "ply"])
async def play_handler(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 and not message.reply_to_message:
        return await message.edit_text("ℹ️ **Usage:** .play <song name / youtube link>")

    query = args[1] if len(args) > 1 else message.reply_to_message.text or ""
    await message.edit_text(f"🔍 [ ꜱᴇᴀʀᴄʜɪɴɢ : {query} ]")

    # 1. Search YouTube
    info = await search_youtube(query)
    if not info:
        return await message.edit_text("❌ **No results found for this song!**")

    title = info["title"]
    duration = format_duration(info["duration"])
    vid = info["id"]

    await message.edit_text(f"⚡ [ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴀ ʏᴜᴋɪ ᴀᴘɪ... ]")

    # 2. Download via Yuki API
    file_path = await download_song(vid)
    if not file_path or not os.path.exists(file_path):
        return await message.edit_text("❌ **Audio download failed! Please try again.**")

    # 3. Stream to VC
    await message.edit_text("🎵 [ ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴠᴄ... ]")
    res = await play_audio_stream(message.chat.id, file_path)

    if res:
        card = format_card(
            "now playing",
            [
                ("track", title[:35] + ("..." if len(title) > 35 else "")),
                ("duration", duration),
                ("source", "YouTube (Yuki API)"),
                ("status", "Streaming in VC 🔊")
            ]
        )
        await message.edit_text(card)
    else:
        await message.edit_text("❌ **Failed to stream in VC.** Ensure Voice Chat is started in this group!")


@on_cmd(["stop"])
async def stop_handler(client, message):
    await message.edit_text("🔄 **Stopping playback...**")
    res = await leave_call(message.chat.id)
    if res:
        await message.edit_text("⏹️ **Playback stopped and left Voice Chat.**")
    else:
        await message.edit_text("❌ **Could not stop or not currently playing in VC.**")


@on_cmd(["song", "music"])
async def song_handler(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.edit_text("ℹ️ **Usage:** .song <song name> or .music <song name>")

    query = args[1]
    await message.edit_text(f"🔍 [ ꜱᴇᴀʀᴄʜɪɴɢ : {query} ]")

    info = await search_youtube(query)
    if not info:
        return await message.edit_text("❌ **Song not found!**")

    title = info["title"]
    duration = info["duration"]
    vid = info["id"]

    await message.edit_text("📥 [ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴘ3... ]")
    file_path = await download_song(vid)

    if not file_path or not os.path.exists(file_path):
        return await message.edit_text("❌ **Failed to download song.**")

    await message.edit_text("📤 [ ᴜᴘʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ... ]")

    try:
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_path,
            title=title,
            performer="Yuki API Music",
            duration=duration,
            caption=f"🎵 **{title}**\n⏱️ Duration: {format_duration(duration)}"
        )
        await message.delete()
    except Exception as e:
        await message.edit_text(f"❌ **Upload Error:** {e}")

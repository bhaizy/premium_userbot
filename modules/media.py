import os
from pyrogram import Client, filters
from core.client import on_cmd
from helpers.ui import format_card, to_small_caps
import config

@on_cmd(["photo", "save"])
async def photo_save_handler(client, message):
    args = message.text.split()
    is_photo_cmd = args[0].endswith("photo")
    action = args[1].lower() if len(args) > 1 else ""

    if is_photo_cmd and action != "save":
        return await message.edit_text("ℹ️ **Usage:** Reply to any photo/video/self-destruct media with .photo save or .save")

    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.video or reply.document or reply.animation or reply.voice):
        return await message.edit_text("❌ **Reply to a photo, video, or disappearing media to save it.**")

    await message.edit_text("⏳ [ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ... ]")

    # Download media to local disk
    try:
        file_path = await client.download_media(reply, file_name=config.DOWNLOAD_DIR)
        if not file_path or not os.path.exists(file_path):
            return await message.edit_text("❌ **Failed to download media.**")

        await message.edit_text("📤 [ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ... ]")

        # Determine sender info for caption
        sender = reply.from_user.first_name if reply.from_user else "Unknown"
        caption = f"💾 **{to_small_caps('saved media')}**\n├─ **From:** {sender}\n└─ **Chat:** {message.chat.title or 'Private Chat'}"

        # Send to Saved Messages ('me')
        if reply.photo:
            await client.send_photo("me", photo=file_path, caption=caption)
        elif reply.video:
            await client.send_video("me", video=file_path, caption=caption)
        elif reply.voice:
            await client.send_voice("me", voice=file_path, caption=caption)
        else:
            await client.send_document("me", document=file_path, caption=caption)

        # Cleanup local file
        try:
            os.remove(file_path)
        except Exception:
            pass

        await message.edit_text("✅ **Media saved permanently to your Saved Messages!** 🔒")
    except Exception as e:
        await message.edit_text(f"❌ **Save Error:** {e}")

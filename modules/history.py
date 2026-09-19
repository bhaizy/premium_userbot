import asyncio
from pyrogram import Client, filters
from core.client import on_cmd
from helpers.ui import format_card, to_small_caps

@on_cmd(["history", "sg"])
async def history_handler(client, message):
    user_id = None
    first_name = "User"

    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        args = message.text.split()
        if len(args) > 1:
            try:
                user_id = int(args[1])
                first_name = str(user_id)
            except ValueError:
                # Try getting user by username
                try:
                    u = await client.get_users(args[1])
                    user_id = u.id
                    first_name = u.first_name
                except Exception:
                    return await message.edit_text("❌ **User not found!**")

    if not user_id:
        return await message.edit_text("ℹ️ **Usage:** Reply to a user with .history or .history <user_id/username>")

    await message.edit_text(f"🔍 [ ꜰᴇᴛᴄʜɪɴɢ ʜɪꜱᴛᴏʀʏ ꜰᴏʀ : {first_name} ]")

    bot_username = "SangMata_BOT"
    try:
        # Send query to SangMata_BOT
        sent_msg = await client.send_message(bot_username, f"/search_id {user_id}")
        await asyncio.sleep(2.5)

        # Retrieve response
        response_text = None
        async for msg in client.get_chat_history(bot_username, limit=3):
            if msg.id > sent_msg.id and msg.text:
                response_text = msg.text
                break

        if not response_text:
            return await message.edit_text("❌ **No response from SangMata Bot. Try again later.**")

        # Format and display
        header = f"**亗 {to_small_caps('name history')} 亗**\n"
        output = f"{header}\n👤 **User:** {first_name} ({user_id})\n\n{response_text}"
        await message.edit_text(output)
    except Exception as e:
        await message.edit_text(f"❌ **History Error:** {e}")

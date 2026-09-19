from pyrogram import Client, filters
from core.client import app, on_cmd
from core.database import add_gmute, remove_gmute, is_gmuted, get_gmutes
from helpers.ui import format_card, to_small_caps

@on_cmd(["gmute"])
async def gmute_handler(client, message):
    user_id = None
    user_name = "User"
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        args = message.text.split()
        if len(args) > 1:
            try:
                user_id = int(args[1])
                user_name = str(user_id)
            except ValueError:
                return await message.edit_text("❌ **Provide a valid User ID or reply to their message.**")

    if not user_id:
        return await message.edit_text("ℹ️ **Usage:** Reply to a user with .gmute or .gmute <user_id>")

    me = await client.get_me()
    if user_id == me.id:
        return await message.edit_text("⚠️ **You cannot gmute yourself!**")

    await add_gmute(user_id)
    card = format_card(
        "global mute",
        [
            ("target", user_name),
            ("user id", str(user_id)),
            ("scope", "All Groups & PMs"),
            ("action", "Auto-Delete Messages")
        ],
        footer="User will be silenced globally."
    )
    await message.edit_text(card)


@on_cmd(["ungmute"])
async def ungmute_handler(client, message):
    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    else:
        args = message.text.split()
        if len(args) > 1:
            try:
                user_id = int(args[1])
            except ValueError:
                return await message.edit_text("❌ **Provide a valid User ID or reply to their message.**")

    if not user_id:
        return await message.edit_text("ℹ️ **Usage:** Reply to a user with .ungmute or .ungmute <user_id>")

    await remove_gmute(user_id)
    await message.edit_text(f"✅ **Ungmuted:** {user_id}. Their messages will no longer be deleted.")


@on_cmd(["gmutelist"])
async def gmutelist_handler(client, message):
    gmutes = get_gmutes()
    if not gmutes:
        return await message.edit_text("ℹ️ **No users are currently globally muted.**")

    text = "🔇 **Globally Muted Users:**\n"
    for uid in gmutes:
        text += f"• {uid}\n"
    await message.edit_text(text)


# Background listener for Gmute (highest priority group=0)
@app.on_message(~filters.me & filters.incoming, group=0)
async def gmute_auto_delete_listener(client, message):
    if not message.from_user:
        return

    if is_gmuted(message.from_user.id):
        try:
            await message.delete()
        except Exception:
            pass

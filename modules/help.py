from pyrogram import Client, filters
from core.client import on_cmd
from helpers.ui import to_small_caps
import config

HELP_TEXT = f"""
╔══════════════════════════╗
   亗 **{to_small_caps('premium userbot help')}** 亗
╚══════════════════════════╝

⚡ **{to_small_caps('system commands')}**
├─ .ping - Check latency, CPU, and uptime
├─ .pong - Inverse ping check
└─ .alive - Detailed userbot status

🎵 **{to_small_caps('vc & music')}**
├─ .play <query> - Play song in VC (via Yuki API)
├─ .stop - Stop VC playback & leave call
├─ .vc join - Join group voice chat
├─ .vc leave - Leave group voice chat
└─ .song <name> - Download & send 320kbps MP3

🔥 **{to_small_caps('raid & spam')}**
├─ .raid <count> <text> - Send multiple messages
├─ .rd / .replyraid - Activate automatic reply-roast
├─ .rrd / .dreplyraid - Stop reply raid on user
└─ .delay <seconds> - Configure raid delay interval

🔇 **{to_small_caps('admin & moderation')}**
├─ .gmute - Global mute user across all groups
├─ .ungmute - Remove user from global mute
└─ .gmutelist - List all globally muted users

💾 **{to_small_caps('tools & media')}**
├─ .photo save / .save - Save self-destructing media to Saved Messages
├─ .history - Check Sangmata name/username history
└─ .help - Show this menu

Prefixes Supported: {" ".join(config.PREFIXES)}
"""

@on_cmd(["help"])
async def help_handler(client, message):
    await message.edit_text(HELP_TEXT)

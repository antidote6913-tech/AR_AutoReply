import os
import time

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.session import StringSession


API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

app = Client(
    "AR_AutoReply",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# =========================
# SETTINGS
# =========================

auto_reply = False

reply_text = (
    "👋 Hello!\n\n"
    "Abhi main available nahi hoon.\n"
    "Message mil gaya hai ✅"
)

# Same person ko baar-baar reply na ho
last_reply = {}
REPLY_COOLDOWN = 60


# =========================
# COMMANDS
# =========================

@app.on_message(filters.me & filters.command("on", prefixes="/"))
async def turn_on(client, message):
    global auto_reply

    auto_reply = True

    await message.edit_text(
        "🟢 **Auto Reply ON**\n\n"
        "Ab incoming private messages ka automatic reply hoga."
    )


@app.on_message(filters.me & filters.command("off", prefixes="/"))
async def turn_off(client, message):
    global auto_reply

    auto_reply = False

    await message.edit_text(
        "🔴 **Auto Reply OFF**"
    )


@app.on_message(filters.me & filters.command("status", prefixes="/"))
async def status(client, message):
    status_text = "🟢 ON" if auto_reply else "🔴 OFF"

    await message.edit_text(
        f"🤖 **AR AutoReply Manager**\n\n"
        f"Status: {status_text}\n"
        f"Cooldown: `{REPLY_COOLDOWN}s`"
    )


@app.on_message(filters.me & filters.command("reply", prefixes="/"))
async def show_reply(client, message):
    await message.edit_text(
        f"💬 **Current Auto Reply:**\n\n{reply_text}"
    )


@app.on_message(filters.me & filters.command("setreply", prefixes="/"))
async def set_reply(client, message):
    global reply_text

    text = message.text or ""

    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        await message.edit_text(
            "❌ Reply text missing.\n\n"
            "Example:\n"
            "`/setreply Hello 👋 Main abhi busy hoon.`"
        )
        return

    reply_text = parts[1]

    await message.edit_text(
        f"✅ **Auto Reply Updated!**\n\n"
        f"{reply_text}"
    )


@app.on_message(filters.me & filters.command("id", prefixes="/"))
async def get_id(client, message):
    chat = message.chat

    await message.edit_text(
        f"🆔 **Chat ID:** `{chat.id}`\n"
        f"👤 **Your ID:** `{message.from_user.id}`"
    )


@app.on_message(filters.me & filters.command("help", prefixes="/"))
async def help_command(client, message):
    await message.edit_text(
        "🤖 **AR AutoReply Manager**\n\n"
        "⚙️ Commands:\n\n"
        "`/on` - Auto reply ON\n"
        "`/off` - Auto reply OFF\n"
        "`/status` - Check status\n"
        "`/reply` - Show current reply\n"
        "`/setreply TEXT` - Change reply\n"
        "`/id` - Get chat ID\n"
        "`/help` - Show this menu"
    )


# =========================
# AUTO REPLY
# =========================

@app.on_message(
    filters.private
    & ~filters.me
    & ~filters.bot
)
async def auto_reply_handler(client, message):
    global auto_reply

    if not auto_reply:
        return

    if not message.from_user:
        return

    user_id = message.from_user.id

    current_time = time.time()
    previous_time = last_reply.get(user_id, 0)

    # Cooldown
    if current_time - previous_time < REPLY_COOLDOWN:
        return

    last_reply[user_id] = current_time

    try:
        await message.reply_text(reply_text)

    except FloodWait as e:
        print(f"FloodWait: waiting {e.value} seconds")
        await __import__("asyncio").sleep(e.value)

    except Exception as e:
        print(f"Auto reply error: {e}")


# =========================
# START
# =========================

print("================================")
print("🤖 AR AutoReply Manager")
print("🚀 Starting...")
print("================================")

app.run()

from pyrogram import Client
from pyrogram.session import StringSession

API_ID = int(input("Enter API_ID: "))
API_HASH = input("Enter API_HASH: ")

with Client(
    StringSession(""),
    api_id=API_ID,
    api_hash=API_HASH
) as app:

    print("\n================================")
    print("YOUR SESSION STRING")
    print("================================\n")

    print(app.export_session_string())

    print("\n================================")
    print("Copy this SESSION_STRING")
    print("================================")

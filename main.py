import os
import asyncio
from pyrogram import Client
from pymongo import MongoClient

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
target_username = "@HEVCFapFilesbot"

SESSIONS = [
    os.environ.get("SESSION_1"),
    os.environ.get("SESSION_2"),
    os.environ.get("SESSION_3"),
]

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["fap_bot"]
collection = db["session_progress"]

async def send_command(session_str, user_id):
    async with Client(name=str(user_id), api_id=api_id, api_hash=api_hash, session_string=session_str) as app:
        entry = collection.find_one({"user_id": user_id})
        last_sent_id = entry["last_sent_id"] if entry else 1

        print(f"[{user_id}] Starting from ID {last_sent_id}")

        for i in range(last_sent_id, last_sent_id + 100):
            try:
                await app.send_message(chat_id=target_username, text=f"/get {i}")
                print(f"[{user_id}] Sent /get {i}")
                await asyncio.sleep(3)
            except Exception as e:
                print(f"[{user_id}] Failed to send /get {i}: {e}")
                await asyncio.sleep(3)

        collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_sent_id": last_sent_id + 100}},
            upsert=True,
        )
        print(f"[{user_id}] Updated progress to ID {last_sent_id + 100}")

async def main():
    tasks = [
        send_command(SESSIONS[0], user_id=1),
        send_command(SESSIONS[1], user_id=2),
        send_command(SESSIONS[2], user_id=3),
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

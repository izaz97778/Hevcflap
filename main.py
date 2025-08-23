from fastapi import FastAPI
import asyncio
import os
import nest_asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from pymongo import MongoClient

nest_asyncio.apply()
app = FastAPI()

# Telegram API
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Load sessions from environment
SESSIONS = [
    os.getenv("SESSION1"),
    os.getenv("SESSION2"),
    os.getenv("SESSION3")
]

target_username = os.getenv("TARGET_USERNAME", "@HEVCFapFilesbot")

# Mongo
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = 'telegram_bot'
COLLECTION_NAME = 'forward_progress'

MESSAGES_PER_RUN = 100
BATCH_SIZE = 100
DELAY_BETWEEN_MESSAGES = 3.2
DELAY_BETWEEN_BATCHES = 0

client_db = MongoClient(MONGO_URI)
db = client_db[DB_NAME]
collection = db[COLLECTION_NAME]

def get_last_sent_id():
    state = collection.find_one({'_id': 'progress'})
    if state:
        return state.get('last_sent_id', 0) + 1
    else:
        collection.insert_one({'_id': 'progress', 'last_sent_id': 0})
        return 1

def update_last_sent_id(msg_id):
    collection.update_one({'_id': 'progress'}, {'$set': {'last_sent_id': msg_id}}, upsert=True)

async def send_from_session(session_string, start_id, end_id, account_index):
    tg_client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await tg_client.start()

    print(f"🧾 Account {account_index+1} sending /get {start_id} to /get {end_id}")
    ids = list(range(start_id, end_id + 1))
    last_id = start_id - 1

    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i + BATCH_SIZE]
        print(f"Account {account_index+1} → Batch {i // BATCH_SIZE + 1}")
        for msg_id in batch:
            try:
                await tg_client.send_message(target_username, f"/get {msg_id}")
                print(f"✅ Account {account_index+1} sent: /get {msg_id}")
                last_id = msg_id
                await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
            except Exception as e:
                print(f"⚠️ Error (Account {account_index+1} /get {msg_id}): {e}")
        if i + BATCH_SIZE < len(ids):
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)

    await tg_client.disconnect()
    return last_id

async def run_all():
    base_start_id = get_last_sent_id()
    tasks = []

    for idx, session in enumerate(SESSIONS):
        if session:  # Only run if session string is present
            start_id = base_start_id + (idx * MESSAGES_PER_RUN)
            end_id = start_id + MESSAGES_PER_RUN - 1
            tasks.append(send_from_session(session, start_id, end_id, idx))

    results = await asyncio.gather(*tasks)
    if results:
        highest_sent_id = max(results)
        update_last_sent_id(highest_sent_id)
        print(f"\n✅ Updated last_sent_id to {highest_sent_id}")

# 🔁 Periodic task loop every 24 hours
async def periodic_runner():
    while True:
        await run_all()
        print("⏱️ Sleeping for 24 hours...")
        await asyncio.sleep(86400)  # 24 hours

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_runner())

@app.get("/")
async def root():
    return {"status": "Bot is running"}

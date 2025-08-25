Here’s a README.md file for your FastAPI-based Telegram automation bot that uses Telethon, MongoDB, and periodic batch messaging:


---

# 🚀 Telegram Batch Message Sender Bot (FastAPI + Telethon)

This is a FastAPI-based Telegram bot that uses multiple Telegram sessions to batch-send `/get <id>` messages to a target user/channel using the **Telethon** library. It keeps track of sent message IDs using **MongoDB** and sends messages in parallel across multiple Telegram accounts.

---

## 🧩 Features

- ✅ Sends `/get <id>` messages using multiple Telegram sessions
- ✅ Keeps track of the last sent message ID using MongoDB
- ✅ Sends messages in configurable batches and delays
- ✅ Automatically runs every 24 hours using an async background task
- ✅ Lightweight API with health check (`GET /`)
- ✅ Easy to deploy via Docker, Koyeb, etc.

---

## ⚙️ Environment Variables

You must set the following environment variables:

```env
# Telegram API credentials
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash

# Telegram target username (user, channel, or bot)
TARGET_USERNAME=@targetusername

# Session strings (generate with Telethon)
SESSION1=session_string_1
SESSION2=session_string_2
SESSION3=session_string_3

# MongoDB URI for saving progress
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net


---

🏗️ Project Structure

.
├── main.py             # FastAPI server and Telegram logic
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it!


---

📦 Requirements

Install dependencies:

pip install -r requirements.txt

requirements.txt should include:

fastapi
uvicorn
telethon
nest_asyncio
pymongo


---

🧪 Run Locally

uvicorn main:app --host 0.0.0.0 --port 8000

Check the bot is live at:

http://localhost:8000/


---

⏱️ Behavior

Each session sends 100 messages per run (/get 1 to /get 100, /get 101 to /get 200, etc.)

Delay between each message: 5 seconds

Delay between batches: 0 seconds

Automatically resumes from the last sent ID

Runs every 24 hours



---

🐳 Dockerfile (Optional)

To containerize:

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Build and run:

docker build -t tg-batch-bot .
docker run -e API_ID=... -e API_HASH=... -e SESSION1=... -e MONGO_URI=... tg-batch-bot


---

💬 Notes

You can increase or decrease MESSAGES_PER_RUN, BATCH_SIZE, DELAY_BETWEEN_MESSAGES in the script.

All messages are sent as /get <id> — this can be customized in the script.

MongoDB is used to resume sending from the last successful ID.



---

🙏 Credits

Built with FastAPI

Telegram API via Telethon

Persistence with MongoDB



---

📄 License

MIT

---

Let me know if you want this converted into a file or need a deployment guide for Koyeb, Railway, or Heroku.


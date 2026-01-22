import os
import asyncio
import random
from pyrogram import Client
from pyrogram.errors import FloodWait
from num2words import num2words

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GROUP = os.getenv("GROUP")

TOTAL = 10000
SAVE_FILE = "last.txt"

EMOJIS = ["😁", "😂", "😅", "🔥", "🥲", "😎", "💀", "🤡", "🫠"]

# ---------- RESUME SYSTEM ----------
def get_last():
    if os.path.exists(SAVE_FILE):
        return int(open(SAVE_FILE).read().strip())
    return 0

def save_last(n):
    with open(SAVE_FILE, "w") as f:
        f.write(str(n))

# ---------- BOT ----------
app = Client(
    "punishment_session",
    api_id=API_ID,
    api_hash=API_HASH
)

async def start():
    last = get_last()
    print("Resume from:", last + 1)

    async with app:
        for i in range(last + 1, TOTAL + 1):
            try:
                hindi = num2words(i, lang="hi")

                # 🎲 random emoji sometimes
                if random.randint(1, 4) == 1:
                    emoji = random.choice(EMOJIS)
                    msg = f"{i} — {hindi} {emoji}"
                else:
                    msg = f"{i} — {hindi}"

                await app.send_message(GROUP, msg)
                print("Sent:", i)
                save_last(i)

                # 🕐 SAFE SPEED (15+ HOURS)
                delay = random.uniform(4.5, 7.5)
                await asyncio.sleep(delay)

                # ☕ human break
                if i % 150 == 0:
                    rest = random.randint(90, 240)
                    print("Break:", rest, "sec")
                    await asyncio.sleep(rest)

            except FloodWait as e:
                print("FloodWait:", e.value)
                await asyncio.sleep(e.value + 15)

            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(60)

asyncio.run(start())

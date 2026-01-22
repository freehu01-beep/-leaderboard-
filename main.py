import os, asyncio, random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from num2words import num2words

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID"))  # 🔐 your telegram id

TOTAL = 10000
SAVE_FILE = "last.txt"
CFG_FILE = "config.txt"

EMOJIS = ["😁","😂","😅","🔥","🥲","😎","🤡","🫠"]

# --------- STORAGE ----------
def get_last():
    if os.path.exists(SAVE_FILE):
        return int(open(SAVE_FILE).read().strip())
    return 0

def save_last(n):
    open(SAVE_FILE,"w").write(str(n))

def get_group():
    if os.path.exists(CFG_FILE):
        return open(CFG_FILE).read().strip()
    return None

def set_group(g):
    open(CFG_FILE,"w").write(g)

PAUSED = False

app = Client("punishment_session", api_id=API_ID, api_hash=API_HASH)

# -------- OWNER COMMANDS --------

@app.on_message(filters.user(OWNER_ID) & filters.command("setgroup"))
async def setgrp(_, m):
    if len(m.command) < 2:
        return await m.reply("Use: /setgroup -100xxxx or link")
    set_group(m.command[1])
    await m.reply("✅ Group updated")

@app.on_message(filters.user(OWNER_ID) & filters.command("pause"))
async def pause(_, m):
    global PAUSED
    PAUSED = True
    await m.reply("⏸ Paused")

@app.on_message(filters.user(OWNER_ID) & filters.command("resume"))
async def resume(_, m):
    global PAUSED
    PAUSED = False
    await m.reply("▶️ Resumed")

@app.on_message(filters.user(OWNER_ID) & filters.command("reset"))
async def reset(_, m):
    save_last(0)
    await m.reply("🔁 Reset to 1")

@app.on_message(filters.user(OWNER_ID) & filters.command("status"))
async def status(_, m):
    await m.reply(f"📊 Current: {get_last()}")

# --------- COUNT LOOP ----------

async def counter():
    await app.start()
    print("Started")

    while True:
        if PAUSED:
            await asyncio.sleep(10)
            continue

        group = get_group()
        if not group:
            await asyncio.sleep(10)
            continue

        i = get_last() + 1
        if i > TOTAL:
            print("Completed")
            break

        try:
            hindi = num2words(i, lang="hi")

            if random.randint(1,4) == 1:
                msg = f"{i} — {hindi} {random.choice(EMOJIS)}"
            else:
                msg = f"{i} — {hindi}"

            await app.send_message(group, msg)
            save_last(i)
            print("Sent:", i)

            await asyncio.sleep(random.uniform(4.5,7.5))

            if i % 150 == 0:
                await asyncio.sleep(random.randint(90,240))

        except FloodWait as e:
            await asyncio.sleep(e.value + 10)
        except Exception as e:
            print("Err:", e)
            await asyncio.sleep(60)

    await app.stop()

app.loop.run_until_complete(counter())

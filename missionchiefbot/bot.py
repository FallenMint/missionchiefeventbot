import discord
from discord.ext import commands, tasks
import random
import json
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv()

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("DISCORD_TOKEN")

COOLDOWN_CHANNEL_ID = 1515313354992914469

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN in .env")

# ======================
# BOT SETUP
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

UK_TZ = pytz.timezone("Europe/London")

# ======================
# DATA
# ======================

UK_LOCATIONS = [
    "London", "Birmingham", "Manchester", "Liverpool", "Leeds",
    "Sheffield", "Bristol", "Nottingham", "Newcastle", "Glasgow",
    "Cardiff", "Belfast",
]

EVENTS = [
    "Section 60",
    "Pandemic",
    "Autumn Weather",
    "Spring Weather",
    "Summer Weather",
    "Sport Weather",
]

LSM_TYPES = [
    "Mass Casualty Response",
    "Large Scale Fire Incident",
    "Multi-Vehicle Pileup",
    "Citywide Emergency",
    "Major Infrastructure Failure"
]

SCENARIOS = [
    "Motorway Collision",
    "High Rise Fire",
    "Chemical Leak",
    "Train Derailment",
    "Stadium Incident",
    "Warehouse Fire",
    "Flood Rescue",
    "Aircraft Crash"
]

MISSION_SUMMARIES = {
    "Motorway Collision": "Multi-vehicle motorway collision with trapped casualties.",
    "High Rise Fire": "High-rise building fire requiring evacuation.",
    "Chemical Leak": "Hazardous chemical leak at industrial site.",
    "Train Derailment": "Passenger train derailment with casualties.",
    "Stadium Incident": "Major incident at large public event.",
    "Warehouse Fire": "Large warehouse fire spreading rapidly.",
    "Flood Rescue": "Severe flooding requiring evacuations.",
    "Aircraft Crash": "Aircraft crash with multi-agency response."
}

# ======================
# WEEKLY STORAGE
# ======================

WEEKLY_FILE = "weekly.json"


def load_weekly():
    if not os.path.exists(WEEKLY_FILE):
        return {"last": 0}
    with open(WEEKLY_FILE, "r") as f:
        return json.load(f)


def save_weekly(data):
    with open(WEEKLY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ======================
# GENERATORS
# ======================

def generate_mission():
    scenario = random.choice(SCENARIOS)
    return f"""🚨 MISSION ALERT 🚨

Scenario: {scenario}
Location: {random.choice(UK_LOCATIONS)}

Summary:
{MISSION_SUMMARIES[scenario]}
"""

def generate_event():
    return f"""🌍 EVENT ALERT 🌍

Type: {random.choice(EVENTS)}
Location: {random.choice(UK_LOCATIONS)}
"""

# ======================
# DAILY ALLIANCE TASK
# ======================

@tasks.loop(minutes=1)
async def daily_alliance():

    now = datetime.now(UK_TZ)

    # 12:00 UK time
    if now.hour == 12 and now.minute == 0:

        channel = bot.get_channel(COOLDOWN_CHANNEL_ID)
        if not channel:
            return

        scenario = random.choice(SCENARIOS)

        await channel.send(f"""🚨 DAILY ALLIANCE EVENT 🚨

Scenario: {scenario}
Location: {random.choice(UK_LOCATIONS)}

Prepare units for activation.
""")

# ======================
# WEEKLY LSM / EVENT TASK
# ======================

@tasks.loop(minutes=5)
async def weekly_event():

    data = load_weekly()
    now = datetime.now(UK_TZ).timestamp()

    if now - data["last"] >= 7 * 86400:

        channel = bot.get_channel(COOLDOWN_CHANNEL_ID)
        if not channel:
            return

        if random.choice([True, False]):
            content = f"""🌪️ WEEKLY LSM EVENT 🌪️

Type: {random.choice(LSM_TYPES)}
Location: {random.choice(UK_LOCATIONS)}
"""
        else:
            content = f"""🚨 WEEKLY EVENT 🚨

Type: {random.choice(EVENTS)}
Location: {random.choice(UK_LOCATIONS)}
"""

        await channel.send(content)

        data["last"] = now
        save_weekly(data)

# ======================
# COMMANDS
# ======================

@bot.command()
async def test(ctx):
    await ctx.send(generate_mission())

@bot.command()
async def testevent(ctx):
    await ctx.send(generate_event())

# ======================
# STARTUP
# ======================

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    if not daily_alliance.is_running():
        daily_alliance.start()

    if not weekly_event.is_running():
        weekly_event.start()

# ======================
# RUN
# ======================

bot.run(TOKEN)

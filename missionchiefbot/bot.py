import discord
from discord.ext import commands, tasks
import random
import json
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1515313354992914469

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
# HELPERS
# ======================

def get_channel():
    return bot.get_channel(CHANNEL_ID)

# ======================
# GENERATORS
# ======================

def mission():
    s = random.choice(SCENARIOS)
    return f"""🚨 MISSION ALERT 🚨

Scenario: {s}
Location: {random.choice(UK_LOCATIONS)}

Summary:
{MISSION_SUMMARIES[s]}
"""

def event():
    return f"""🌍 EVENT ALERT 🌍

Type: {random.choice(EVENTS)}
Location: {random.choice(UK_LOCATIONS)}
"""

def lsm():
    return f"""🌪️ LSM EVENT 🌪️

Type: {random.choice(LSM_TYPES)}
Location: {random.choice(UK_LOCATIONS)}
"""

# ======================
# AUTOMATION
# ======================

@tasks.loop(minutes=1)
async def daily_alliance():

    now = datetime.now(UK_TZ)

    if now.hour == 12 and now.minute == 0:
        channel = get_channel()
        if channel:
            s = random.choice(SCENARIOS)
            await channel.send(f"""🚨 ALLIANCE EVENT 🚨

Scenario: {s}
Location: {random.choice(UK_LOCATIONS)}

Prepare for activation.
""")

@tasks.loop(minutes=5)
async def weekly_lsm():

    now = datetime.now(UK_TZ)

    # Simple weekly trigger (same weekday/time logic optional upgrade later)
    if now.weekday() == 6 and now.hour == 18 and now.minute < 5:
        channel = get_channel()
        if channel:
            await channel.send(lsm())

# ======================
# COMMANDS
# ======================

@bot.command()
async def mission(ctx):
    await ctx.send(mission())

@bot.command()
async def event(ctx):
    await ctx.send(event())

@bot.command()
async def lsm_cmd(ctx):
    await ctx.send(lsm())

@bot.command()
async def alliance(ctx):
    s = random.choice(SCENARIOS)
    await ctx.send(f"""🚨 ALLIANCE EVENT (MANUAL) 🚨

Scenario: {s}
Location: {random.choice(UK_LOCATIONS)}
""")

# ======================
# STARTUP
# ======================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    if not daily_alliance.is_running():
        daily_alliance.start()

    if not weekly_lsm.is_running():
        weekly_lsm.start()

# ======================
# RUN
# ======================

bot.run(TOKEN)

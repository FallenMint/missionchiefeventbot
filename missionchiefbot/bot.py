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

# ======================
# STATE STORAGE
# ======================

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_daily": "", "last_weekly": 0}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ======================
# HELPERS
# ======================

def get_channel():
    return bot.get_channel(CHANNEL_ID)

# ======================
# MESSAGE BUILDERS
# ======================

def alliance_event():
    return f"""🚨 ALLIANCE EVENT 🚨

Scenario: {random.choice(SCENARIOS)}
Location: {random.choice(UK_LOCATIONS)}

Prepare for activation.
"""

def lsm_event():
    return f"""🌪️ LSM EVENT 🌪️

Type: {random.choice(LSM_TYPES)}
Location: {random.choice(UK_LOCATIONS)}
"""

# ======================
# BUTTONS (CRITICAL PART)
# ======================

class EventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Alliance Event",
        style=discord.ButtonStyle.green,
        emoji="🚨",
        custom_id="alliance_btn"
    )
    async def alliance_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(alliance_event(), ephemeral=True)

    @discord.ui.button(
        label="LSM Event",
        style=discord.ButtonStyle.red,
        emoji="🌪️",
        custom_id="lsm_btn"
    )
    async def lsm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(lsm_event(), ephemeral=True)

# ======================
# DAILY ALLIANCE (12:00 UK)
# ======================

@tasks.loop(minutes=1)
async def daily_alliance():

    now = datetime.now(UK_TZ)
    state = load_state()

    today = now.strftime("%Y-%m-%d")

    if now.hour == 12 and now.minute == 0:

        if state["last_daily"] != today:

            ch = get_channel()
            if ch:
                await ch.send(
                    alliance_event(),
                    view=EventView()   # ✅ BUTTONS ATTACHED
                )

            state["last_daily"] = today
            save_state(state)

# ======================
# WEEKLY LSM (7 DAY CYCLE)
# ======================

@tasks.loop(minutes=5)
async def weekly_lsm():

    state = load_state()
    now = datetime.now(UK_TZ).timestamp()

    if now - state["last_weekly"] >= 7 * 86400:

        ch = get_channel()
        if ch:
            await ch.send(
                lsm_event(),
                view=EventView()   # ✅ BUTTONS ATTACHED
            )

        state["last_weekly"] = now
        save_state(state)

# ======================
# COMMANDS
# ======================

@bot.command()
async def alliance(ctx):
    await ctx.send(alliance_event(), view=EventView())

@bot.command()
async def lsm(ctx):
    await ctx.send(lsm_event(), view=EventView())

@bot.command()
async def event(ctx):
    await ctx.send(f"🌍 EVENT\n\nLocation: {random.choice(UK_LOCATIONS)}")

@bot.command()
async def mission(ctx):
    await ctx.send(f"🚨 MISSION\n\nScenario: {random.choice(SCENARIOS)}")

# ======================
# STARTUP
# ======================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # REQUIRED for persistent buttons
    bot.add_view(EventView())

    if not daily_alliance.is_running():
        daily_alliance.start()

    if not weekly_lsm.is_running():
        weekly_lsm.start()

# ======================
# RUN
# ======================

bot.run(TOKEN)

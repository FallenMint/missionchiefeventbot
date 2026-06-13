import discord
from discord.ext import commands, tasks
import random
import os
import json
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
    "London","Birmingham","Manchester","Liverpool","Leeds",
    "Sheffield","Bristol","Nottingham","Newcastle","Glasgow",
    "Cardiff","Belfast"
]

EVENTS = [
    "Section 60",
    "Pandemic",
    "Autumn Weather",
    "Spring Weather",
    "Summer Weather",
    "Sport Weather"
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
# CHANNEL
# ======================
def get_channel():
    return bot.get_channel(CHANNEL_ID)

# ======================
# MESSAGES
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
# BUTTONS (FIXED + PERSISTENT)
# ======================
class EventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Alliance Event",
        style=discord.ButtonStyle.green,
        custom_id="alliance_button"
    )
    async def alliance_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(alliance_event(), ephemeral=True)

    @discord.ui.button(
        label="LSM Event",
        style=discord.ButtonStyle.red,
        custom_id="lsm_button"
    )
    async def lsm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(lsm_event(), ephemeral=True)

# ======================
# DAILY EVENT (12:00 UK)
# ======================
@tasks.loop(minutes=1)
async def daily_task():
    now = datetime.now(UK_TZ)

    if now.hour == 12 and now.minute == 0:
        ch = get_channel()
        if ch:
            await ch.send(alliance_event(), view=EventView())

# ======================
# WEEKLY EVENT (7 DAYS)
# ======================
@tasks.loop(minutes=5)
async def weekly_task():
    now = datetime.now(UK_TZ).timestamp()

    # simple weekly timer (7 days)
    if not hasattr(weekly_task, "last"):
        weekly_task.last = 0

    if now - weekly_task.last > 604800:
        ch = get_channel()
        if ch:
            await ch.send(lsm_event(), view=EventView())

        weekly_task.last = now

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
async def test(ctx):
    await ctx.send("Buttons test below:", view=EventView())

# ======================
# STARTUP
# ======================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # REQUIRED for buttons to appear on restart
    bot.add_view(EventView())

    if not daily_task.is_running():
        daily_task.start()

    if not weekly_task.is_running():
        weekly_task.start()

# ======================
# RUN
# ======================
bot.run(TOKEN)

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
# COOLDOWNS
# ======================
COOLDOWN_FILE = "cooldowns.json"

ONE_DAY = 86400
ONE_WEEK = 604800


def load_cooldowns():
    if not os.path.exists(COOLDOWN_FILE):
        return {"alliance": 0, "lsm": 0}
    with open(COOLDOWN_FILE, "r") as f:
        return json.load(f)


def save_cooldowns(data):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ======================
# DATA
# ======================
UK_LOCATIONS = [
    "London", "Birmingham", "Manchester", "Liverpool", "Leeds",
    "Sheffield", "Bristol", "Nottingham", "Newcastle", "Glasgow",
    "Cardiff", "Belfast"
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

LSM_TYPES = [
    "Mass Casualty Response",
    "Large Scale Fire Incident",
    "Multi-Vehicle Pileup",
    "Citywide Emergency",
    "Major Infrastructure Failure"
]


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
# BUTTON VIEW
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

        data = load_cooldowns()
        now = datetime.now().timestamp()

        remaining = ONE_DAY - (now - data["alliance"])

        if remaining > 0:
            h = int(remaining // 3600)
            m = int((remaining % 3600) // 60)

            return await interaction.response.send_message(
                f"⏳ Alliance cooldown active: **{h}h {m}m remaining**",
                ephemeral=True
            )

        data["alliance"] = now
        save_cooldowns(data)

        await interaction.response.send_message(alliance_event(), ephemeral=True)

    @discord.ui.button(
        label="LSM Event",
        style=discord.ButtonStyle.red,
        custom_id="lsm_button"
    )
    async def lsm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):

        data = load_cooldowns()
        now = datetime.now().timestamp()

        remaining = ONE_WEEK - (now - data["lsm"])

        if remaining > 0:
            d = int(remaining // 86400)
            h = int((remaining % 86400) // 3600)

            return await interaction.response.send_message(
                f"⏳ LSM cooldown active: **{d}d {h}h remaining**",
                ephemeral=True
            )

        data["lsm"] = now
        save_cooldowns(data)

        await interaction.response.send_message(lsm_event(), ephemeral=True)


# ======================
# COMMANDS
# ======================
@bot.command()
async def test(ctx):
    await ctx.send("Event Panel:", view=EventView())


@bot.command()
async def alliance(ctx):
    await ctx.send(alliance_event(), view=EventView())


@bot.command()
async def lsm(ctx):
    await ctx.send(lsm_event(), view=EventView())


# ======================
# STARTUP
# ======================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # keeps buttons working after restart
    bot.add_view(EventView())


# ======================
# RUN
# ======================
bot.run(TOKEN)

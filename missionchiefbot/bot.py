import discord
from discord.ext import commands
import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1515313354992914469

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN")

# ======================
# BOT SETUP
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# COOLDOWNS
# ======================
COOLDOWN_FILE = "cooldowns.json"

ALLIANCE_CD = 60 * 60 * 24      # 24 hours
LSM_CD = 60 * 60 * 24 * 7       # 7 days


def load_cooldowns():
    if not os.path.exists(COOLDOWN_FILE):
        return {"alliance": 0, "lsm": 0}

    try:
        with open(COOLDOWN_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"alliance": 0, "lsm": 0}

    data.setdefault("alliance", 0)
    data.setdefault("lsm", 0)

    return data


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
# EVENT GENERATORS
# ======================
def make_alliance_event():
    return f"""🚨 ALLIANCE EVENT 🚨

Scenario: {random.choice(SCENARIOS)}
Location: {random.choice(UK_LOCATIONS)}

Status: Ready for deployment.
"""


def make_lsm_event():
    return f"""🌪️ LSM EVENT 🌪️

Type: {random.choice(LSM_TYPES)}
Location: {random.choice(UK_LOCATIONS)}

Status: Major mobilisation required.
"""

# ======================
# VIEW (BUTTONS)
# ======================
class EventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # ----------------------
    # ALLIANCE BUTTON
    # ----------------------
    @discord.ui.button(label="Alliance Event", style=discord.ButtonStyle.green)
    async def alliance(self, interaction: discord.Interaction, button: discord.ui.Button):

        data = load_cooldowns()
        now = datetime.now().timestamp()

        remaining = ALLIANCE_CD - (now - data["alliance"])

        if data["alliance"] != 0 and remaining > 0:
            h = int(remaining // 3600)
            m = int((remaining % 3600) // 60)

            return await interaction.response.send_message(
                f"⏳ Alliance cooldown: **{h}h {m}m remaining**",
                ephemeral=True
            )

        data["alliance"] = now
        save_cooldowns(data)

        await interaction.response.send_message(make_alliance_event(), ephemeral=True)

    # ----------------------
    # LSM BUTTON
    # ----------------------
    @discord.ui.button(label="LSM Event", style=discord.ButtonStyle.red)
    async def lsm(self, interaction: discord.Interaction, button: discord.ui.Button):

        data = load_cooldowns()
        now = datetime.now().timestamp()

        remaining = LSM_CD - (now - data["lsm"])

        if data["lsm"] != 0 and remaining > 0:
            d = int(remaining // 86400)
            h = int((remaining % 86400) // 3600)

            return await interaction.response.send_message(
                f"⏳ LSM cooldown: **{d}d {h}h remaining**",
                ephemeral=True
            )

        data["lsm"] = now
        save_cooldowns(data)

        await interaction.response.send_message(make_lsm_event(), ephemeral=True)

# ======================
# COMMANDS
# ======================
@bot.command()
async def panel(ctx):
    await ctx.send("🎛️ Event Control Panel", view=EventView())

@bot.command()
async def test(ctx):
    await ctx.send("Testing buttons:", view=EventView())

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

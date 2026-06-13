import discord
from discord.ext import commands, tasks
import random
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# =======================
# CONFIG
# =======================
TOKEN = os.getenv("DISCORD_TOKEN")

COOLDOWN_CHANNEL_ID = 1515313354992914469

COOLDOWN_FILE = "cooldowns.json"
PANEL_FILE = "panel.json"

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN in .env")

# =======================
# BOT SETUP
# =======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =======================
# YOUR DATA
# =======================

UK_LOCATIONS = [
    "London", "Birmingham", "Manchester", "Liverpool", "Leeds",
    "Sheffield", "Bristol", "Nottingham", "Newcastle", "Glasgow",
    "Cardiff", "Belfast",
]

EVENTS = [
    "Storm",
    "Section 60",
    "Pandemic",
    "Autumn Weather",
    "Spring Weather",
    "Summer Weather",
    "Sport Weather",
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

COASTAL = ["Liverpool", "Bristol", "Cardiff", "Belfast", "Glasgow", "Newcastle"]

MISSION_SUMMARIES = {
    "Motorway Collision": "A major multi-vehicle collision has occurred on a busy motorway.",
    "High Rise Fire": "A serious fire has broken out in a high-rise building.",
    "Chemical Leak": "A hazardous chemical release has been reported at an industrial site.",
    "Train Derailment": "A passenger train has derailed, leaving several carriages damaged.",
    "Stadium Incident": "A major incident has occurred during a large public event.",
    "Warehouse Fire": "A large warehouse is engulfed in flames.",
    "Flood Rescue": "Severe flooding has affected the area.",
    "Aircraft Crash": "An aircraft has crashed resulting in a large-scale response."
}

# =======================
# JSON HELPERS
# =======================

def load_json(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# =======================
# MISSION / EVENT GENERATION
# =======================

def generate_mission():
    scenario = random.choice(SCENARIOS)
    location = random.choice(UK_LOCATIONS)

    return {
        "scenario": scenario,
        "location": location,
        "summary": MISSION_SUMMARIES[scenario],
        "units": {
            "Fire Engines": random.randint(15, 35),
            "Police Cars": random.randint(20, 50),
            "Ambulance Officers": random.randint(5, 15),
        },
        "patients": random.randint(20, 100),
        "prisoners": random.randint(10, 70)
    }

def generate_event():
    location = random.choice(UK_LOCATIONS)
    area = "Coastal Area" if location in COASTAL else "Urban Area"

    return {
        "event": random.choice(EVENTS),
        "location": location,
        "area": area
    }

# =======================
# FORMATTERS
# =======================

def format_mission(m):
    units = "\n".join(f"{k} x{v}" for k, v in m["units"].items())

    return f"""🚨 MISSION ALERT 🚨

Scenario: {m['scenario']}
Location: {m['location']}

Summary:
{m['summary']}

Units:
{units}

Patients: {m['patients']}
Prisoners: {m['prisoners']}
"""

def format_event(e):
    return f"""🌍 EVENT ALERT 🌍

Type: {e['event']}
Location: {e['location']}
Area: {e['area']}
"""

# =======================
# COOLDOWNS SYSTEM
# =======================

def get_status():
    data = load_json(COOLDOWN_FILE, {})
    now = datetime.utcnow().timestamp()

    alliance = "✅ READY"
    storm = "✅ READY"

    if "alliance" in data:
        remaining = data["alliance"] - now
        if remaining > 0:
            alliance = f"⏳ {int(remaining // 3600)}h {int((remaining % 3600) // 60)}m"

    if "storm" in data:
        remaining = data["storm"] - now
        if remaining > 0:
            storm = f"⏳ {int(remaining // 86400)}d {int((remaining % 86400) // 3600)}h"

    return f"""📋 EVENT COOLDOWN PANEL

🚨 Alliance Event
{alliance}

🌪️ Storm
{storm}

Click a button when completed.
"""

class CooldownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Alliance Complete",
        style=discord.ButtonStyle.green,
        emoji="🚨",
        custom_id="alliance_btn"
    )
    async def alliance(self, interaction, button):

        data = load_json(COOLDOWN_FILE, {})
        ready = datetime.utcnow() + timedelta(hours=24)

        data["alliance"] = ready.timestamp()
        save_json(COOLDOWN_FILE, data)

        await interaction.response.send_message(
            f"Alliance cooldown started. Ready <t:{int(ready.timestamp())}:R>",
            ephemeral=True
        )

        await update_panel()

    @discord.ui.button(
        label="Storm Complete",
        style=discord.ButtonStyle.blurple,
        emoji="🌪️",
        custom_id="storm_btn"
    )
    async def storm(self, interaction, button):

        data = load_json(COOLDOWN_FILE, {})
        ready = datetime.utcnow() + timedelta(days=7)

        data["storm"] = ready.timestamp()
        save_json(COOLDOWN_FILE, data)

        await interaction.response.send_message(
            f"Storm cooldown started. Ready <t:{int(ready.timestamp())}:R>",
            ephemeral=True
        )

        await update_panel()

# =======================
# PANEL SYSTEM
# =======================

async def update_panel():
    channel = bot.get_channel(COOLDOWN_CHANNEL_ID)
    if not channel:
        return

    panel = load_json(PANEL_FILE, {})

    try:
        if "message_id" in panel:
            msg = await channel.fetch_message(panel["message_id"])
            await msg.edit(content=get_status(), view=CooldownView())
        else:
            raise Exception()
    except:
        msg = await channel.send(get_status(), view=CooldownView())
        save_json(PANEL_FILE, {"message_id": msg.id})

# =======================
# BACKGROUND CHECK
# =======================

@tasks.loop(minutes=1)
async def cooldown_checker():

    data = load_json(COOLDOWN_FILE, {})
    now = datetime.utcnow().timestamp()

    channel = bot.get_channel(COOLDOWN_CHANNEL_ID)
    if not channel:
        return

    changed = False

    if "alliance" in data and now >= data["alliance"]:
        await channel.send("🚨 Alliance Event is now AVAILABLE!")
        del data["alliance"]
        changed = True

    if "storm" in data and now >= data["storm"]:
        await channel.send("🌪️ Storm is now AVAILABLE!")
        del data["storm"]
        changed = True

    if changed:
        save_json(COOLDOWN_FILE, data)
        await update_panel()

# =======================
# COMMANDS
# =======================

@bot.command()
async def test(ctx):
    await ctx.send(format_mission(generate_mission()))

@bot.command()
async def testevent(ctx):
    await ctx.send(format_event(generate_event()))

# =======================
# STARTUP
# =======================

@bot.event
async def on_ready():
    bot.add_view(CooldownView())

    await update_panel()

    if not cooldown_checker.is_running():
        cooldown_checker.start()

    print(f"Logged in as {bot.user}")

# =======================
# RUN BOT
# =======================

bot.run(TOKEN)

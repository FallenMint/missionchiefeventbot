import discord
from discord.ext import commands
import random

from config import TOKEN, CHANNEL_ID, UK_LOCATIONS, UNITS, EVENTS, RULES_TEXT

# -----------------------------
# INTENTS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# SCENARIOS
# -----------------------------
SCENARIOS = [
    "Multi-vehicle motorway collision with entrapment",
    "High-rise residential fire with casualties",
    "Gas main explosion in urban area",
    "Large stadium crowd disorder incident",
    "Chemical leak at industrial site",
    "Severe flooding with stranded civilians",
    "Armed response to active threat",
    "Train derailment with mass casualties",
    "Warehouse fire with collapse risk",
    "Storm damage causing multiple emergencies"
]

# -----------------------------
# GENERATORS
# -----------------------------
def generate_mission():
    return {
        "name": random.choice(SCENARIOS),
        "location": random.choice(UK_LOCATIONS),
        "units": random.sample(UNITS, k=10)
    }

def generate_event():
    return {
        "name": f"{random.choice(EVENTS)} Major Incident",
        "location": random.choice(UK_LOCATIONS),
        "units": random.sample(UNITS, k=12)
    }

# -----------------------------
# FORMATTERS
# -----------------------------
def format_mission(m):
    return (
        f"🚨 **LARGE SCALE MISSION** 🚨\n\n"
        f"📛 Scenario: {m['name']}\n"
        f"📍 Location: {m['location']}\n\n"
        f"🚒 Units Required:\n" +
        "\n".join(f"- {u}" for u in m['units']) +
        f"\n\n📊 Rules:\n{RULES_TEXT}"
    )

def format_event(e):
    return (
        f"🌍 **WEEKLY MAJOR EVENT** 🌍\n\n"
        f"📛 Event: {e['name']}\n"
        f"📍 Location: {e['location']}\n\n"
        f"🟦 Area: Large Rectangular Operational Zone\n"
        f"⏱ Call Volume: 30 seconds\n\n"
        f"🚨 Units Required:\n" +
        "\n".join(f"- {u}" for u in e['units'])
    )

# -----------------------------
# COMMANDS
# -----------------------------
@bot.command()
async def test(ctx):
    """Generate a test mission"""
    m = generate_mission()
    await ctx.send(format_mission(m))

@bot.command()
async def testevent(ctx):
    """Generate a test event"""
    e = generate_event()
    await ctx.send(format_event(e))

# -----------------------------
# RUN BOT
# -----------------------------
bot.run(TOKEN)

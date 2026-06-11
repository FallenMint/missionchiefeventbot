import discord
from discord.ext import commands
import random

from config import TOKEN, UK_LOCATIONS, EVENTS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

def generate_mission():
    return {
        "scenario": random.choice(SCENARIOS),
        "location": random.choice(UK_LOCATIONS),
        "units": {
            "Fire Engines": random.randint(8, 25),
            "Aerial Appliance Trucks": random.randint(1, 4),
            "Fire Officers": random.randint(4, 10),
            "Police Cars": random.randint(15, 40),
            "Armed Response": random.randint(0, 6),
            "Traffic Cars": random.randint(2, 10),
            "Ambulance Officers": 1,
            "Mass Casualty Equipment": 1
        },
        "prisoners": random.randint(0, 100),
        "patients": random.randint(0, 100),
    }

def generate_event():
    loc = random.choice(UK_LOCATIONS)
    area = "Large Area"
    if loc in COASTAL:
        area = "Medium Coastal Area"

    return {
        "event": random.choice(EVENTS),
        "location": loc,
        "area": area
    }

def format_mission(m):
    units = "\n".join([f"{k} x{v}" for k, v in m["units"].items()])
    return f"""🚨 MISSION 🚨

Scenario: {m['scenario']}
Location: {m['location']}

Units:
{units}

Patients: {m['patients']}
Prisoners: {m['prisoners']}
"""

def format_event(e):
    return f"""🌍 EVENT 🌍

Type: {e['event']}
Location: {e['location']}
Area: {e['area']}
"""

@bot.command()
async def test(ctx):
    await ctx.send(format_mission(generate_mission()))

@bot.command()
async def testevent(ctx):
    await ctx.send(format_event(generate_event()))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)

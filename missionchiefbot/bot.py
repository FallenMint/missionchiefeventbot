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

COASTAL = [
    "Liverpool",
    "Bristol",
    "Cardiff",
    "Belfast",
    "Glasgow",
    "Newcastle"
]

MISSION_SUMMARIES = {
    "Motorway Collision":
        "A major multi-vehicle collision has occurred on a busy motorway. Multiple casualties are trapped and emergency services are conducting large-scale rescue operations while managing severe traffic disruption.",

    "High Rise Fire":
        "A serious fire has broken out in a high-rise building. Fire crews are carrying out rescues, evacuating residents, and preventing the fire from spreading to neighbouring properties.",

    "Chemical Leak":
        "A hazardous chemical release has been reported at an industrial site. Specialist teams are monitoring contamination levels while emergency services establish exclusion zones.",

    "Train Derailment":
        "A passenger train has derailed, leaving several carriages damaged. Emergency services are rescuing passengers and treating a large number of casualties.",

    "Stadium Incident":
        "A major incident has occurred during a large public event. Emergency responders are dealing with crowd management, casualties, and scene security.",

    "Warehouse Fire":
        "A large warehouse is engulfed in flames. Fire crews are tackling the blaze while protecting nearby buildings and searching for anyone trapped inside.",

    "Flood Rescue":
        "Severe flooding has affected the area. Rescue teams are evacuating residents, assisting stranded civilians, and protecting critical infrastructure.",

    "Aircraft Crash":
        "An aircraft has crashed resulting in a large-scale multi-agency response. Rescue operations are underway and casualty clearing stations have been established."
}

def generate_mission():
    scenario = random.choice(SCENARIOS)
    location = random.choice(UK_LOCATIONS)

    return {
        "scenario": scenario,
        "location": location,
        "summary": MISSION_SUMMARIES[scenario],
        "units": {
            "Fire Engines": random.randint(15, 35),
            "Aerial Appliance Trucks": random.randint(2, 6),
            "Fire Officers": random.randint(5, 12),
            "Police Cars": random.randint(20, 50),
            "Armed Response": random.randint(0, 8),
            "Traffic Cars": random.randint(4, 12),
            "Ambulance Officers": 1,
            "Mass Casualty Equipment": 1
        },
        "patients": 100,
        "prisoners": random.randint(50, 70)
    }

def generate_event():
    location = random.choice(UK_LOCATIONS)

    area = "Large Area"
    if location in COASTAL:
        area = "Medium Coastal Area"

    return {
        "event": random.choice(EVENTS),
        "location": location,
        "area": area
    }

def format_mission(m):
    units = "\n".join(f"{k} x{v}" for k, v in m["units"].items())

    return f"""🚨 MISSION ALERT 🚨

Scenario: {m['scenario']}
Location: {m['location']}

Summary:
{m['summary']}

Required Units:
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

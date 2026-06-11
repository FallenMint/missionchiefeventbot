import discord
from discord.ext import commands
import random

from config import TOKEN, UK_LOCATIONS, EVENTS

# -----------------------------

# BOT SETUP

# -----------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------

# SCENARIOS

# -----------------------------

SCENARIOS = [
"Multi-Vehicle Motorway Collision",
"High Rise Residential Fire",
"Industrial Chemical Leak",
"Train Derailment",
"Large Shopping Centre Fire",
"Aircraft Crash",
"Warehouse Fire",
"Prison Riot",
"Large Stadium Disorder",
"Gas Main Explosion",
"Building Collapse",
"Flood Rescue Operation",
"Storm Damage Incident",
"Major Ferry Terminal Incident",
"Active Armed Threat",
]

COASTAL_LOCATIONS = [
"Liverpool",
"Bristol",
"Cardiff",
"Belfast",
"Glasgow",
"Newcastle",
]

# -----------------------------

# MISSION GENERATOR

# -----------------------------

def generate_mission():
return {
"scenario": random.choice(SCENARIOS),
"location": random.choice(UK_LOCATIONS),

```
    "units": {
        "Fire Engines": random.randint(8, 30),
        "Aerial Appliance Trucks": random.randint(1, 6),
        "Fire Officers": random.randint(4, 10),
        "Ambulance Control Units": random.randint(1, 3),
        "BSU": random.randint(1, 4),
        "Hazmat": random.randint(0, 3),
        "Rescue Support": random.randint(1, 5),
        "Foam Unit": random.randint(0, 3),
        "Police Cars": random.randint(15, 40),
        "Armed Response": random.randint(0, 8),
        "DSU": random.randint(1, 5),
        "Traffic Cars": random.randint(2, 10),
        "Police Helicopters": random.randint(0, 2),
        "OTL": random.randint(1, 4),
        "PRV": random.randint(2, 10),
        "SRV": random.randint(2, 8),
        "Welfare": random.randint(1, 3),
        "ATV": random.randint(0, 4),

        # ALWAYS INCLUDED
        "Mass Casualty Equipment": 1,
        "Ambulance Officers": 1,
    },

    "prisoners": random.randint(0, 100),
    "patients": random.randint(0, 100),
}
```

# -----------------------------

# EVENT GENERATOR

# -----------------------------

def generate_event():
location = random.choice(UK_LOCATIONS)

```
area_size = "Large Rectangular Area"

if location in COASTAL_LOCATIONS:
    area_size = "Medium Rectangular Area"

return {
    "event": random.choice(EVENTS),
    "location": location,
    "area": area_size,
}
```

# -----------------------------

# FORMATTERS

# -----------------------------

def format_mission(mission):
units_text = ""

```
for unit, amount in mission["units"].items():
    if amount > 0:
        units_text += f"• {unit} x{amount}\n"

return (
    f"🚨 **LARGE SCALE MISSION** 🚨\n\n"
    f"📛 Scenario: {mission['scenario']}\n"
    f"📍 Location: {mission['location']}\n\n"
    f"🚒 Units Required:\n{units_text}\n"
    f"👮 Possible Prisoners: {mission['prisoners']}\n"
    f"🚑 Possible Patients: {mission['patients']}\n"
    f"🚚 Transport Probability: 80%\n"
    f"🏥 Hospital Department: General Internal\n"
    f"🩺 Critical Care Quote: 0"
)
```

def format_event(event):
return (
f"🌍 **WEEKLY MAJOR EVENT** 🌍\n\n"
f"📛 Event Type: {event['event']}\n"
f"📍 Location: {event['location']}\n"
f"🟦 Area: {event['area']}\n"
f"⏱️ Call Volume: Every 30 Seconds\n\n"
f"Mission generation handled by MissionChief."
)

# -----------------------------

# COMMANDS

# -----------------------------

@bot.command()
async def test(ctx):
mission = generate_mission()
await ctx.send(format_mission(mission))

@bot.command()
async def testevent(ctx):
event = generate_event()
await ctx.send(format_event(event))

# -----------------------------

# READY EVENT

# -----------------------------

@bot.event
async def on_ready():
print(f"Logged in as {bot.user}")

# -----------------------------

# START BOT

# -----------------------------

bot.run(TOKEN)

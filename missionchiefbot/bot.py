import discord
from discord.ext import commands
import random

from config import TOKEN, CHANNEL_ID, UK_LOCATIONS, EVENTS, RULES_TEXT

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
"Storm damage causing multiple emergencies",
"Large shopping centre fire",
"Aircraft crash near populated area",
"Industrial explosion",
"Major ferry terminal incident",
"Large prison disturbance",
"Collapsed building with multiple casualties",
]

COASTAL_LOCATIONS = [
"Liverpool",
"Bristol",
"Cardiff",
"Belfast",
"Glasgow",
"Newcastle"
]

# -----------------------------

# MISSION GENERATION

# -----------------------------

def generate_mission():
units = {
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

```
    # ALWAYS INCLUDED
    "Mass Casualty Equipment": 1,
    "Ambulance Officers": 1,
}

return {
    "name": random.choice(SCENARIOS),
    "location": random.choice(UK_LOCATIONS),
    "units": units,
    "prisoners": random.randint(0, 100),
    "patients": random.randint(0, 100),
}
```

# -----------------------------

# EVENT GENERATION

# -----------------------------

def generate_event():
location = random.choice(UK_LOCATIONS)

```
area_size = "Large Rectangular Operational Zone"

if location in COASTAL_LOCATIONS:
    area_size = "Medium Rectangular Operational Zone"

return {
    "name": f"{random.choice(EVENTS)} Major Event",
    "location": location,
    "area": area_size
}
```

# -----------------------------

# FORMATTERS

# -----------------------------

def format_mission(m):
unit_text = "\n".join(
f"- {unit} x{amount}"
for unit, amount in m["units"].items()
if amount > 0
)

```
return (
    f"🚨 **LARGE SCALE MISSION** 🚨\n\n"
    f"📛 Scenario: {m['name']}\n"
    f"📍 Location: {m['location']}\n\n"
    f"🚒 Units Required:\n{unit_text}\n\n"
    f"👮 Possible Prisoners: {m['prisoners']}\n"
    f"🚑 Possible Patients: {m['patients']}\n"
    f"🚑 Transport Probability: 80%\n"
    f"🏥 Hospital Department: General Internal\n"
    f"🩺 Critical Care Quote: 0"
)
```

def format_event(e):
return (
f"🌍 **WEEKLY MAJOR EVENT** 🌍\n\n"
f"📛 Event: {e['name']}\n"
f"📍 Location: {e['location']}\n\n"
f"🟦 Area: {e['area']}\n"
f"⏱ Call Volume: Every 30 Seconds\n\n"
f"Mission generation will be handled by MissionChief."
)

# -----------------------------

# COMMANDS

# -----------------------------

@bot.command()
async def test(ctx):
await ctx.send(format_mission(generate_mission()))

@bot.command()
async def testevent(ctx):
await ctx.send(format_event(generate_event()))

@bot.event
async def on_ready():
print(f"Logged in as {bot.user}")

# -----------------------------

# RUN

# -----------------------------

bot.run(TOKEN)
